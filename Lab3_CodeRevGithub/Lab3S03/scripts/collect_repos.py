import os
import json
import random
import time
import requests
import pandas as pd
from tqdm import tqdm
import sys
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from config_token import configurar_token

TOKEN = configurar_token()

BASE_DIR = os.path.join("Lab3_CodeRevGithub", "Lab3S03")
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

output_csv = os.path.join(DATA_DIR, "selected_repos.csv")
output_json = os.path.join(DATA_DIR, "selected_repos.json")

print(f"🔑 Caminho onde os arquivos serão salvos:")
print(f"   📄 CSV: {output_csv}")
print(f"   📄 JSON: {output_json}\n")
print("-" * 120 + "\n")

def format_seconds(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

def mover_pycache(destino="Lab3_CodeRevGithub/Lab3S03/__pycache__"):
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            origem = os.path.join(root, "__pycache__")
            if os.path.abspath(origem) == os.path.abspath(destino):
                continue
            os.makedirs(destino, exist_ok=True)
            for arquivo in os.listdir(origem):
                arquivo_destino = os.path.join(destino, arquivo)
                if os.path.exists(arquivo_destino):
                    os.remove(arquivo_destino)
                shutil.move(os.path.join(origem, arquivo), destino)
            shutil.rmtree(origem)
            print(f"📦 Pycache movido para: {destino}")

def handle_rate_limit(response, fallback_wait=600, max_wait=1800, message="", error=None):
    if message:
        print(f"\n⚠️ {message}")
    if error:
        print(f"🔍 Erro: {type(error).__name__} — {error}")

    wait_seconds = None
    status_info = ""

    try:
        status_code = response.status_code
        reason = response.reason
        status_info = f"{status_code} — {reason}"

        if status_code == 403 and int(response.headers.get("X-RateLimit-Remaining", 1)) == 0:
            reset_timestamp = int(response.headers.get("X-RateLimit-Reset", time.time() + fallback_wait))
            now = int(time.time())
            wait_seconds = max(reset_timestamp - now + 10, 10)
    except Exception as e:
        status_info = f"{type(e).__name__} — {e}"
        wait_seconds = random.randint(fallback_wait, max_wait)

    if wait_seconds:
        if wait_seconds > max_wait:
            wait_seconds = random.randint(fallback_wait, max_wait)

        print(f"⚠ Erro ao consultar limite da API: {status_info}")
        print(f"🚦 Limite de requisições da API atingido — Iniciando pausa temporária.")
        print(f"⏳ Estimativa de espera: {wait_seconds} segundos até a liberação de novas requisições...\n")
        time.sleep(wait_seconds)
        return True

    return False

def filter_repos_with_min_prs(token, min_prs=100, needed=200):
    headers_rest = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    headers_graphql = {
        "Authorization": f"bearer {token}"
    }

    all_filtered = []
    page = 1

    print(f"🔍 Iniciando coleta de repositórios com +1000 estrelas e pelo menos {min_prs} pull requests fechados com *reviews*...\n")

    while len(all_filtered) < needed:
        params = {
            "q": "stars:>1000",
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
            "page": page
        }

        response = requests.get("https://api.github.com/search/repositories", headers=headers_rest, params=params)
        if handle_rate_limit(response):
            continue

        if response.status_code != 200:
            print(f"Erro na página {page}: {response.status_code}")
            break

        repos = response.json().get("items", [])
        if not repos:
            break

        print(f"🔄 Processando página {page}...")
        validos_na_pagina = 0
        repos_nesta_pagina = []

        for repo in tqdm(repos, desc=f"   ⚙️  Filtrando por PRs com reviews", ncols=120):
            owner, name = repo["full_name"].split("/")
            valid_prs = []
            cursor = None
            fetched = 0
            max_to_fetch = 600

            while fetched < max_to_fetch:
                after_clause = f', after: "{cursor}"' if cursor else ""
                query = {
                    "query": f"""
                    {{
                        repository(owner: \"{owner}\", name: \"{name}\") {{
                            pullRequests(states: [MERGED, CLOSED], first: 100{after_clause}, orderBy: {{field: CREATED_AT, direction: DESC}}) {{
                                nodes {{
                                    reviews {{ totalCount }}
                                }}
                                pageInfo {{ hasNextPage endCursor }}
                            }}
                        }}
                    }}
                    """
                }

                try:
                    r = requests.post("https://api.github.com/graphql", headers=headers_graphql, json=query)
                    if handle_rate_limit(r):
                        continue
                    response_json = r.json()

                    if "errors" in response_json:
                        break

                    pr_data = response_json["data"]["repository"]["pullRequests"]
                    for pr in pr_data["nodes"]:
                        if pr["reviews"]["totalCount"] > 0:
                            valid_prs.append(pr)

                    fetched += len(pr_data["nodes"])
                    if not pr_data["pageInfo"]["hasNextPage"]:
                        break
                    cursor = pr_data["pageInfo"]["endCursor"]

                except Exception as e:
                    break

            pr_count = len(valid_prs)
            if pr_count >= min_prs:
                repo["pr_count"] = pr_count
                validos_na_pagina += 1
                repos_nesta_pagina.append(repo)


        all_filtered.extend(repos_nesta_pagina)

        print(f"   📄 Página {page} finalizada.")
        print(f"      ➕ Extraídos nesta página: {validos_na_pagina}")
        print(f"      📊 Total acumulado: {len(all_filtered)} repositórios válidos.")

        # Estatísticas da página
        faixas = [
            (0, 99),
            (100, 199),
            (200, 499),
            (500, 999),
            (1000, float("inf"))
        ]

        contexto = f"página {page}"
        pr_counts = [(repo.get("full_name", "desconhecido"), repo.get("pr_count", 0)) for repo in repos_nesta_pagina if "pr_count" in repo]

        print(f"\n📊 Distribuição dos repositórios por faixas de PRs válidos ({contexto}):")
        for min_val, max_val in faixas:
            label = f"{int(min_val)}+" if max_val == float("inf") else f"{int(min_val)}–{int(max_val)}"
            count = sum(1 for _, pr_count in pr_counts if min_val <= pr_count <= max_val)
            print(f"   🔹 {label} PRs: {count} repositório(s)")

        if pr_counts:
            sorted_repos = sorted(pr_counts, key=lambda x: x[1])
            repo_min = sorted_repos[0]
            repo_max = sorted_repos[-1]

            print(f"\n📈 Estatísticas de PRs nesta página:")
            print(f"   🔹 Mínimo: {repo_min[1]} PRs — {repo_min[0]}")
            print(f"   🔹 Máximo: {repo_max[1]} PRs — {repo_max[0]}")
        else:
            print("\n🔴 Nenhum repositório válido nesta página para calcular estatísticas.")

        print("\n" + "-" * 80 + "\n")

        # Salvar resultados parciais
        if all_filtered:
            selected = [
                "id", "full_name", "description", "language",
                "stargazers_count", "forks_count", "open_issues_count", "pr_count"
            ]
            rows = [{k: r.get(k) for k in selected} for r in all_filtered]
            df = pd.DataFrame(rows)
            df.to_csv(output_csv, index=False, encoding="utf-8")
            with open(output_json, "w", encoding="utf-8") as f:
                json.dump(all_filtered, f, indent=2, ensure_ascii=False)

        page += 1

    if len(all_filtered) == 0:
        print("🔴 Nenhum repositório válido encontrado.")

    return all_filtered[:needed]

def save_repos_to_files(repos, file_path):
    if not repos:
        print("🔴 Nenhum repositório válido coletado. Arquivos não foram salvos.")
        return

    # Define colunas e ordem lógica
    selected = [
        "id", "full_name", "description", "language",
        "stargazers_count", "forks_count", "open_issues_count", "pr_count"
    ]
    rows = [{k: r.get(k) for k in selected} for r in repos]
    df = pd.DataFrame(rows)

    # Limita tamanho da descrição para facilitar visualização
    df["description"] = df["description"].apply(
        lambda x: (x[:300] + "...") if isinstance(x, str) and len(x) > 300 else x
    )

    print(f"\n✅ {len(repos)} repositórios válidos salvos:")

    try:
        # Garante que o diretório existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # ⚠️ Remove arquivos antigos (csv, json, xlsx) se existirem
        for ext in [".csv", ".json"]:
            path_to_remove = file_path.replace(".csv", ext)
            if os.path.exists(path_to_remove):
                os.remove(path_to_remove)

        # Salva CSV com separador ";"
        df.to_csv(file_path, index=False, sep=";", encoding="utf-8")
        print(f"    ✅ Arquivo CSV salvo em {file_path}")

        # Salva como JSON também
        json_path = file_path.replace(".csv", ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(repos, f, indent=2, ensure_ascii=False)
        print(f"    ✅ Arquivo JSON salvo em {json_path}")

    except Exception as e:
        print(f"🔴 Erro ao salvar os arquivos: {e}\n")

def print_faixa_distribuicao(repos, contexto="geral"):
    faixas = [
        (100, 199),
        (200, 499),
        (500, 999),
        (1000, float("inf"))
    ]

    pr_counts = [(repo.get("full_name", "desconhecido"), repo.get("pr_count", 0)) for repo in repos if "pr_count" in repo]

    print(f"\n📊 Distribuição dos repositórios por faixas de PRs válidos ({contexto}):")
    for min_val, max_val in faixas:
        label = f"{int(min_val)}+" if max_val == float("inf") else f"{int(min_val)}–{int(max_val)}"
        count = sum(1 for _, pr_count in pr_counts if min_val <= pr_count <= max_val)
        print(f"   🔹 {label} PRs: {count} repositório(s)")

    if pr_counts:
        sorted_repos = sorted(pr_counts, key=lambda x: x[1])
        repo_min = sorted_repos[0]
        repo_max = sorted_repos[-1]

        minimo = repo_min[1]
        maximo = repo_max[1]

        print(f"\n📈 Estatísticas dos PRs válidos:")
        print(f"   🔹 Mínimo: {minimo}  — {repo_min[0]}")
        print(f"   🔹 Máximo: {maximo}  — {repo_max[0]}")
    else:
        print("\n🔴 Nenhuma informação de PRs disponível para estatísticas.")


def main():
    print("Iniciando o processo de coleta de repositórios...\n")
    start_time = time.time()

    filtered = filter_repos_with_min_prs(TOKEN, min_prs=100, needed=200)

    # ✅ Filtragem final por segurança (mínimo de 100 PRs válidos)
    filtered_final = [repo for repo in filtered if repo.get("pr_count", 0) >= 100]

    print_faixa_distribuicao(filtered_final, contexto="final")

    save_repos_to_files(filtered_final, output_csv)

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"\n⏱️ Tempo total de execução: {format_seconds(elapsed)}")

if __name__ == "__main__":
    main()
    mover_pycache()
