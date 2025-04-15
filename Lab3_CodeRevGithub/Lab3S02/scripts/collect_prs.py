import json
from github import Github
import os
import time
from statistics import mean, median
import pandas as pd
import requests
from tqdm import tqdm
import random
import sys
import shutil
import contextlib
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from config_token import configurar_token

BASE_DIR = os.path.join("Lab3_CodeRevGithub", "Lab3S02")
DATA_DIR = os.path.join(BASE_DIR, "data")
REPO_FILE = os.path.join(DATA_DIR, "selected_repos.csv")
COLLECTED_FILE = os.path.join(DATA_DIR, "collected_prs.csv")
os.makedirs(DATA_DIR, exist_ok=True)

def format_seconds(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

def mover_pycache(destino="Lab3_CodeRevGithub/Lab3S02/__pycache__"):
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            origem = os.path.join(root, "__pycache__")
            if os.path.abspath(origem) == os.path.abspath(destino):
                continue  # already in the right place
            os.makedirs(destino, exist_ok=True)
            for arquivo in os.listdir(origem):
                arquivo_destino = os.path.join(destino, arquivo)
                # Force overwrite by removing the existing file before moving
                if os.path.exists(arquivo_destino):
                    os.remove(arquivo_destino)
                shutil.move(os.path.join(origem, arquivo), destino)
            shutil.rmtree(origem)
            tqdm.write(f"📦 Pycache movido para: {destino}")

def handle_error_and_rate_limit(g, error=None, fallback_wait=600, max_wait=1800):
    wait_seconds = None
    status_info = ""
    handled = False

    try:
        if isinstance(error, Exception):
            status_info = f"{type(error).__name__} — {error}"

            # Verifica se é uma exceção do PyGithub com headers
            if hasattr(error, 'status') or hasattr(error, 'status_code'):
                status_code = getattr(error, 'status', None) or getattr(error, 'status_code', None)
                if status_code == 403:
                    try:
                        core = g.get_rate_limit().core
                        remaining = core.remaining
                        reset_timestamp = core.reset.timestamp()
                        now = time.time()



                        if remaining == 0:
                            wait_seconds = max(int(reset_timestamp - now + 10), 10)
                        else:
                            wait_seconds = random.randint(fallback_wait, max_wait)

                        handled = True
                    except Exception as fallback_check:
                        status_info += f" | Erro ao checar rate limit: {fallback_check}"
                        wait_seconds = random.randint(fallback_wait, max_wait)
                        handled = True


            # Trata timeout, conexão recusada, e erros comuns de rede
            elif isinstance(error, (
                ConnectionError,
                TimeoutError,
                OSError,
                requests.exceptions.RequestException,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                requests.exceptions.Timeout,
                requests.exceptions.TooManyRedirects,
            )):
                wait_seconds = random.randint(60, 180)
                handled = True


            # Catch-all para outros erros — imprime stacktrace para depuração
            else:
                wait_seconds = random.randint(fallback_wait, max_wait)
                handled = True

    except Exception as e:
        status_info = f"Erro ao lidar com erro: {type(e).__name__} — {e}"
        wait_seconds = random.randint(fallback_wait, max_wait)
        handled = True

    if wait_seconds and handled:
        if wait_seconds > max_wait:
            wait_seconds = random.randint(fallback_wait, max_wait)

        tqdm.write(f"\n⚠️ Erro: {status_info}")
        tqdm.write(f"🚦 Limite de requisições da API atingido ou outro erro - Iniciando pausa temporária..")
        tqdm.write(f"⏳ Estimativa de espera: {wait_seconds} segundos até a liberação de novas requisições...\n")
        time.sleep(wait_seconds)
        return True  # Pausou

    return False  # Não pausou (não foi erro esperado)

def collect_prs_from_repo(g, repo_name, min_valid_prs=100, max_valid_prs=None, max_pages=50):
    collected = []
    try:
        repo = g.get_repo(repo_name)
        page = 0
        valid_count = 0
        analisados = 0

        total_prs_fechados = repo.get_pulls(state="closed").totalCount

        with tqdm(ncols=120, bar_format="    ⏳{l_bar}{bar}| {n_fmt} PRs válidos coletados", leave=True, total=total_prs_fechados) as pbar:
            while page < max_pages:
                prs = repo.get_pulls(state="closed", sort="created", direction="desc").get_page(page)

                if not prs:
                    break

                for pr in prs:
                    if max_valid_prs and valid_count >= max_valid_prs:
                        break  # Limite máximo atingido

                    analisados += 1
                    try:
                        if not pr.closed_at:
                            continue

                        time_diff = pr.closed_at - pr.created_at
                        if time_diff.total_seconds() < 3600:
                            continue

                        with contextlib.redirect_stdout(io.StringIO()):
                            reviews = list(pr.get_reviews())
                        if not reviews:
                            continue

                        participants = set()
                        if pr.user and pr.user.login:
                            participants.add(pr.user.login)

                        try:
                            comments = list(pr.get_issue_comments())
                        except:
                            comments = list(pr.get_comments())

                        for comment in comments:
                            if comment.user and comment.user.login:
                                participants.add(comment.user.login)
                        for review in reviews:
                            if review.user and review.user.login:
                                participants.add(review.user.login)

                        collected.append({
                            "repo_name": repo_name,
                            "pr_number": pr.number,
                            "title": pr.title,
                            "body": pr.body or "",
                            "body_length": len(pr.body or ""),
                            "state": pr.state,
                            "merged": pr.merged,
                            "created_at": pr.created_at.isoformat(),
                            "closed_at": pr.closed_at.isoformat(),
                            "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                            "review_count": len(reviews),
                            "files_changed": pr.changed_files,
                            "additions": pr.additions,
                            "deletions": pr.deletions,
                            "comments": pr.comments,
                            "review_comments": pr.review_comments,
                            "time_to_close_hours": time_diff.total_seconds() / 3600,
                            "participant_count": len(participants)
                        })

                        valid_count += 1
                        pbar.total = analisados
                        pbar.update(1)

                    except Exception as e:
                        if handle_error_and_rate_limit(g, error=e):
                            continue
                        else:
                            raise e

                if max_valid_prs and valid_count >= max_valid_prs:
                    break  # Limite máximo atingido

                page += 1

        tqdm.write(f"   🔍 {valid_count} PRs válidos encontrados entre {analisados} PRs avaliados em '{repo_name}'")

        if valid_count < min_valid_prs:
            tqdm.write(f"⚠️ Apenas {valid_count} PRs válidos encontrados em '{repo_name}' — abaixo do mínimo ({min_valid_prs}).")
            return []

        return collected

    except Exception as e:
        if handle_error_and_rate_limit(g, error=e):
            return []
        else:
            raise e

# Função para salvar PRs coletados em CSV
def save_prs_to_files(prs, file_path):
    if not prs:
        print("🔴 Nenhum PR válido coletado. Arquivos não foram salvos.")
        return

    # Define colunas e ordem lógica
    selected = [
        "repo_name", "pr_number", "title", "body", "language",
        "created_at", "closed_at", "merged_at", "state", "merged",
        "review_count", "files_changed", "additions", "deletions",
        "comments", "review_comments", "time_to_close_hours", "participant_count"
    ]
    rows = [{k: r.get(k) for k in selected} for r in prs]
    df = pd.DataFrame(rows)

    # Limita o tamanho do body para facilitar leitura
    df["body"] = df["body"].apply(
        lambda x: (x[:300] + "...") if isinstance(x, str) and len(x) > 300 else x
    )

    print(f"\n   🧮 PRs consolidados atualmente: {len(prs)}")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 👉 Diferente do save_repos: aqui **não removemos arquivos antigos**

        # Salva CSV com separador ";"
        df.to_csv(file_path, index=False, sep=";", encoding="utf-8")
        print(f"       ✅ Arquivo CSV salvo em {file_path}")

        # Salva como JSON
        json_path = file_path.replace(".csv", ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(prs, f, indent=2, ensure_ascii=False)
        print(f"       ✅ Arquivo JSON salvo em {json_path}")

    except Exception as e:
        print(f"🔴 Erro ao salvar os arquivos de PRs: {e}\n")

def load_repos(file_path, required_columns=None):
    if required_columns is None:
        if "selected" in file_path:
            required_columns = ["full_name"]
        else:
            required_columns = [
                "repo_name", "pr_number", "title", "body", "state",
                "merged", "created_at", "closed_at", "merged_at",
                "review_count", "files_changed", "additions", "deletions",
                "comments", "review_comments", "time_to_close_hours", "participant_count"
            ]

    if os.path.exists(file_path):
        for sep in [";", ","]:
            try:
                df = pd.read_csv(file_path, sep=sep)
                check_columns = required_columns.copy()
                if "body_length" in check_columns:
                    check_columns.remove("body_length")
                if all(col in df.columns for col in check_columns):
                    return df
            except Exception:
                continue

    # Se não conseguiu carregar, recria o arquivo
    print(f"⚠️ Arquivo '{file_path}' inválido ou ausente. Criando novo com colunas padrão.")
    df = pd.DataFrame(columns=required_columns)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False, sep=";")
    return df


def repo_has_valid_prs(collected_prs_df, repo_name, min_prs=100, max_prs=1000):
    repo_data = collected_prs_df[collected_prs_df['repo_name'] == repo_name]
    valid_prs = repo_data.dropna(subset=["pr_number", "title", "body", "state", "created_at", "closed_at"])
    return min_prs <= valid_prs.shape[0] <= max_prs

def compare_repositories(selected_repos_df, collected_prs_df, g):
    # Normaliza: converte para string, tira espaços e transforma para minúsculas
    selected_repos = selected_repos_df['full_name'].astype(str).str.strip().str.lower().tolist()
    collected_repos = collected_prs_df['repo_name'].astype(str).str.strip().str.lower().unique().tolist()

    valid_repos = []
    invalid_repos = []

    tqdm.write("    🔍 Verificando Repositórios Selecionados...")
    with tqdm(total=len(selected_repos), ncols=120, 
              bar_format="    ⏳ {l_bar}{bar}| {n:03d}/{total:03d} {percentage:3.0f}% {remaining}",
              leave=True, position=0) as pbar:
        for repo_name in selected_repos:
            try:
                g.get_repo(repo_name)
                valid_repos.append(repo_name)
            except Exception:
                invalid_repos.append(repo_name)
            pbar.update(1)

    removed_repos = [repo for repo in collected_repos if repo not in selected_repos]
    collected_in_selected = [repo for repo in collected_repos if repo in selected_repos]

    complete_repos = []
    incomplete_repos = []

    for repo in collected_in_selected:
        try:
            total_prs_repo = g.get_repo(repo).get_pulls(state="all").totalCount
            is_valid = repo_has_valid_prs(collected_prs_df, repo, min_prs=100, max_prs=total_prs_repo)
            if is_valid:
                complete_repos.append(repo)
            else:
                incomplete_repos.append(repo)
        except Exception as e:
            pass

    return complete_repos, incomplete_repos, len(removed_repos), len(collected_repos), len(collected_in_selected), valid_repos, invalid_repos, removed_repos

def filter_remaining_repos(selected_df, collected_df):
    """
    Retorna uma lista de repositórios selecionados que ainda não foram coletados.
    """
    selected = set(selected_df["full_name"])
    collected = set(collected_df["repo_name"])
    return list(selected - collected)

def show_initial_info():
    tqdm.write(f"📁 Caminho dos repositórios: {REPO_FILE}")
    tqdm.write(f"📁 Caminho dos PRs: {COLLECTED_FILE}\n")
    tqdm.write("-" * 120 + "\n")

def summarize_collection_results(
    selected_repos_df, collected_prs_df,
    complete_repos, incomplete_repos,
    repos_pendentes_set, removidos_set,
    collected_file
):
    total_collected_repos = len(collected_prs_df["repo_name"].unique())

    tqdm.write("\n📊 Resumo da Coleta de PRs\n")
    tqdm.write(f"   📋 Repositórios selecionados: {len(selected_repos_df)}")
    tqdm.write(f"   📋 Repositórios processados: {total_collected_repos}")
    tqdm.write(f"   📋 Repositórios com PRs completos: {len(complete_repos)}")
    tqdm.write(f"   📋 Repositórios com PRs incompletos: {len(incomplete_repos)}")
    tqdm.write(f"   🗑️  Repositórios anteriormente coletados, mas removidos da lista atual: {len(removidos_set)}")
    tqdm.write(f"\n   📋 Repositórios pendentes de coleta: {len(repos_pendentes_set)}\n")
    tqdm.write("-" * 120 + "\n")

    # 🔥 Remove PRs de repositórios que não estão mais na lista selecionada
    if not collected_prs_df.empty:
        selected_set_lower = set(selected_repos_df["full_name"].str.lower().str.strip())
        before = len(collected_prs_df)
        collected_prs_df = collected_prs_df[
            collected_prs_df["repo_name"].str.lower().str.strip().isin(selected_set_lower)
        ].reset_index(drop=True)
        after = len(collected_prs_df)

        if before != after:
            collected_prs_df.to_csv(collected_file, index=False, encoding='utf-8')
            tqdm.write(f"🧹 PRs de repositórios não selecionados foram excluídos ({before - after} linhas removidas).")

    # 🔥 Limita o total de repositórios para no máximo 200
    unique_repos = collected_prs_df["repo_name"].str.lower().str.strip().unique()
    if len(unique_repos) > 200:
        tqdm.write(f"⚠️ Mais de 200 repositórios com PRs detectados ({len(unique_repos)}). Serão mantidos apenas os 200 primeiros.")
        repos_a_manter = list(selected_repos_df["full_name"].str.lower().str.strip())[:200]

        antes = len(collected_prs_df)
        collected_prs_df = collected_prs_df[
            collected_prs_df["repo_name"].str.lower().str.strip().isin(repos_a_manter)
        ].reset_index(drop=True)
        depois = len(collected_prs_df)

        collected_prs_df.to_csv(collected_file, index=False, encoding='utf-8')
        tqdm.write(f"✅ PRs filtrados para manter somente 200 repositórios. ({antes - depois} linhas removidas)")

    return collected_prs_df

def filter_collected_repositories(selected_repos_df, collected_prs_df, output_path) -> pd.DataFrame:
    selected_repos_set = set(selected_repos_df['full_name'].str.lower().str.strip())
    filtered_collected_repos_df = collected_prs_df[
        collected_prs_df['repo_name'].str.lower().str.strip().isin(selected_repos_set)
    ]
    filtered_collected_repos_df = filtered_collected_repos_df.drop_duplicates(subset=["repo_name"])
    filtered_collected_repos_df = filtered_collected_repos_df.head(200)
    filtered_collected_repos_df.to_csv(output_path, index=False, sep=";", encoding="utf-8")
    return filtered_collected_repos_df

# Carregamento dos arquivos CSV
selected_repos_df = pd.read_csv(REPO_FILE, sep=";")
collected_prs_df = pd.read_csv(COLLECTED_FILE, sep=";")

# Chama a função para filtrar os repositórios coletados
output_path = COLLECTED_FILE
filtered_collected_repos_df = filter_collected_repositories(selected_repos_df, collected_prs_df, output_path)

# Retorna o número de repositórios após a filtragem
filtered_collected_repos_df['repo_name'].nunique(), output_path


def coletar_prs_dos_repos(remaining_repos, collected_file, g, incomplete_repos):
    tqdm.write(f"\n📄 Coletando PRs dos repositórios restantes ({len(remaining_repos)})...")
    total_prs_collected = 0
    repo_times = {}

    collected_df = load_repos(collected_file)

    for idx, repo_name in enumerate(remaining_repos):
        tipo_coleta = "♻️  RECOLETA" if repo_name in incomplete_repos else "🆕 NOVO"
        tqdm.write(f"\n🔄 {str(idx + 1).zfill(2)}/{len(remaining_repos)} Coletando PRs de repositório: {repo_name} ({tipo_coleta})")

        inicio = time.time()
        try:
            prs = collect_prs_from_repo(g, repo_name, min_valid_prs=100)
        except Exception as e:
            tqdm.write(f"   ⚠️ Erro ao coletar PRs de '{repo_name}': {e}")
            continue
        fim = time.time()

        tempo = fim - inicio
        repo_times[repo_name] = tempo
        tempo_str = format_seconds(tempo)

        if prs:
            validos = len(prs)
            total_prs_collected += validos
            tqdm.write(f"   📦 PRs válidos coletados de '{repo_name}': {validos} ⏱️ Tempo: {tempo_str}")

            new_df = pd.DataFrame(prs)
            
            if new_df.empty:
                continue
            if collected_df.empty and not new_df.empty:
                collected_df = pd.DataFrame(columns=new_df.columns)

            collected_df = pd.concat([collected_df, new_df], ignore_index=True)

            antes = collected_df.shape[0]
            collected_df.drop_duplicates(subset=["repo_name", "pr_number"], inplace=True)
            depois = collected_df.shape[0]
            removidos = antes - depois
            if removidos > 0:
                tqdm.write(f"   🔍 {removidos} PRs duplicados removidos.")

            save_prs_to_files(collected_df.to_dict(orient="records"), collected_file)
        else:
            tqdm.write(f"   ⚠️ Repositório '{repo_name}' ignorado — menos de 100 PRs válidos. ⏱️ Tempo: {tempo_str}")

    tqdm.write(f"\n📊 Total acumulado de PRs válidos coletados nesta execução: {total_prs_collected}")

    tempos = list(repo_times.values())
    if tempos:
        media_tempo = mean(tempos)
        mediana_tempo = median(tempos)
        tempo_total = sum(tempos)

        tqdm.write(f"\n⏱️ Estatísticas de Tempo da Coleta:")
        tqdm.write(f"   🔹 Tempo total: {format_seconds(tempo_total)}")
        tqdm.write(f"   🔹 Tempo médio por repositório: {format_seconds(media_tempo)}")
        tqdm.write(f"   🔹 Tempo mediano por repositório: {format_seconds(mediana_tempo)}")

def main():
    g = Github(configurar_token())
    selected_repos_df = load_repos(REPO_FILE)
    collected_prs_df = load_repos(COLLECTED_FILE)

    if selected_repos_df.empty or 'full_name' not in selected_repos_df.columns:
        tqdm.write("❌ Arquivo de repositórios selecionados está vazio ou mal formatado. Verifique o arquivo.")
        return

    show_initial_info()

    # 🔃 Filtra os repositórios para garantir no máximo 200 antes de avaliar completude
    filtered_collected_repos_df = filter_collected_repositories(selected_repos_df, collected_prs_df, COLLECTED_FILE)

    # Usa o DataFrame filtrado para verificar completude
    complete_repos, incomplete_repos, _, _, _, _, _, _ = compare_repositories(selected_repos_df, filtered_collected_repos_df, g)

    # Atualiza o DataFrame usado para o restante do fluxo
    collected_prs_df = filtered_collected_repos_df

    # Padroniza nomes de repositórios selecionados
    selected_set = set(selected_repos_df['full_name'].astype(str).str.strip().str.lower())
    collected_set = set(collected_prs_df['repo_name'].astype(str).str.strip().str.lower())
    removidos_set = collected_set - selected_set
    repos_pendentes_set = selected_set - collected_set

    # Atualiza após remoções e resumo
    collected_prs_df = summarize_collection_results(
        selected_repos_df, collected_prs_df,
        complete_repos, incomplete_repos,
        repos_pendentes_set, removidos_set,
        COLLECTED_FILE
    )

    # Filtra repositórios incompletos que ainda estão entre os selecionados
    incomplete_set = {r.strip().lower() for r in incomplete_repos if r.strip().lower() in selected_set}

    # Garante que só os repositórios válidos sejam considerados
    remaining_repos = sorted(list((repos_pendentes_set | incomplete_set) & selected_set))

    if remaining_repos:
        coletar_prs_dos_repos(remaining_repos, COLLECTED_FILE, g, incomplete_repos)
    else:
        tqdm.write("🔴 Não há repositórios restantes para coletar.")

    # Verifica quantos repositórios únicos estão presentes no CSV final
    if os.path.exists(COLLECTED_FILE):
        try:
            final_df = pd.read_csv(COLLECTED_FILE, sep=";")
            repos_unicos = final_df["repo_name"].dropna().str.lower().str.strip().unique()
            tqdm.write(f"\n📦 Total final de repositórios com PRs coletados no CSV: {len(repos_unicos)}")
        except Exception as e:
            tqdm.write(f"\n⚠️ Erro ao ler 'collected_prs.csv': {e}")
    else:
        tqdm.write("\n⚠️ Arquivo 'collected_prs.csv' não encontrado para contagem final de repositórios.")

# === EXECUÇÃO PRINCIPAL ===
if __name__ == "__main__":
    main()
    mover_pycache()
