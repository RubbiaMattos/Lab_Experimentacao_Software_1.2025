import os
import json
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime


def get_github_token():
    token = "TOKEN GITHUB"  # Insira seu token diretamente aqui
    if not token:
        raise ValueError("Token do GitHub não definido")
    return token



def fetch_popular_repos(token, count=200):
    """
    Busca os repositórios mais populares do GitHub.

    Args:
        token (str): Token de autenticação do GitHub
        count (int): Número de repositórios a serem coletados

    Returns:
        list: Lista de dicionários contendo informações dos repositórios
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Parâmetros para buscar os repositórios mais populares
    params = {
        "q": "stars:>1000",  # Filtra por estrelas para garantir popularidade
        "sort": "stars",
        "order": "desc",
        "per_page": 100
    }

    all_repos = []
    pages_to_fetch = (count + 99) // 100  # Calcula quantas páginas precisamos buscar

    for page in tqdm(range(1, pages_to_fetch + 1), desc="Coletando repositórios"):
        params["page"] = page
        response = requests.get(
            "https://api.github.com/search/repositories",
            headers=headers,
            params=params
        )

        if response.status_code != 200:
            print(f"Erro ao buscar repositórios: {response.status_code}")
            print(response.json())
            break

        data = response.json()
        all_repos.extend(data.get("items", []))

        # Verifica se chegamos ao limite de chamadas da API
        if "X-RateLimit-Remaining" in response.headers and int(response.headers["X-RateLimit-Remaining"]) == 0:
            reset_time = int(response.headers["X-RateLimit-Reset"])
            reset_datetime = datetime.fromtimestamp(reset_time)
            current_time = datetime.now()
            wait_time = (reset_datetime - current_time).total_seconds()

            if wait_time > 0:
                print(f"Limite de chamadas da API atingido. Aguardando {wait_time / 60:.2f} minutos...")
                time.sleep(wait_time + 5)  # +5 segundos para garantir

    # Limita ao número exato solicitado
    return all_repos[:count]


def filter_repos_with_min_prs(repos, token, min_prs=100):
    """
    Filtra os repositórios que têm pelo menos um número mínimo de PRs.

    Args:
        repos (list): Lista de repositórios a serem filtrados
        token (str): Token de autenticação do GitHub
        min_prs (int): Número mínimo de PRs (MERGED + CLOSED)

    Returns:
        list: Lista de repositórios filtrados
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    filtered_repos = []

    for repo in tqdm(repos, desc="Filtrando repositórios por número de PRs"):
        full_name = repo["full_name"]

        # Busca o número de PRs fechados (CLOSED + MERGED)
        url = f"https://api.github.com/search/issues?q=repo:{full_name}+is:pr+is:closed&per_page=1"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Erro ao buscar PRs para {full_name}: {response.status_code}")
            continue

        pr_count = response.json().get("total_count", 0)

        if pr_count >= min_prs:
            repo["pr_count"] = pr_count
            filtered_repos.append(repo)
            print(f"Repositório {full_name} adicionado com {pr_count} PRs")

        # Verifica se chegamos ao limite de chamadas da API
        if "X-RateLimit-Remaining" in response.headers and int(response.headers["X-RateLimit-Remaining"]) < 5:
            reset_time = int(response.headers["X-RateLimit-Reset"])
            reset_datetime = datetime.fromtimestamp(reset_time)
            current_time = datetime.now()
            wait_time = (reset_datetime - current_time).total_seconds()

            if wait_time > 0:
                print(f"Quase no limite de chamadas da API. Aguardando {wait_time / 60:.2f} minutos...")
                time.sleep(wait_time + 5)  # +5 segundos para garantir

    return filtered_repos


def save_repos_to_csv(repos, output_file):
    """
    Salva a lista de repositórios em um arquivo CSV.

    Args:
        repos (list): Lista de dicionários com informações dos repositórios
        output_file (str): Caminho do arquivo de saída
    """
    # Selecionando apenas os campos relevantes
    selected_fields = [
        "id", "full_name", "description", "language", "stargazers_count",
        "forks_count", "open_issues_count", "pr_count"
    ]

    # Criando um DataFrame com os campos selecionados
    repo_data = []
    for repo in repos:
        repo_info = {field: repo.get(field, None) for field in selected_fields if field in repo or field == "pr_count"}
        repo_data.append(repo_info)

    df = pd.DataFrame(repo_data)

    # Salvando o DataFrame em um arquivo CSV
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Repositórios salvos em {output_file}")

    # Também salva uma versão completa em JSON para referência
    with open(output_file.replace(".csv", ".json"), "w") as f:
        json.dump(repos, f, indent=2)


def main():
    # Obter token do GitHub
    token = get_github_token()

    # Buscar os repositórios mais populares
    print("Buscando repositórios populares...")
    repos = fetch_popular_repos(token, count=200)
    print(f"Encontrados {len(repos)} repositórios populares.")

    # Filtrar repositórios com pelo menos 100 PRs
    print("Filtrando repositórios com pelo menos 100 PRs...")
    filtered_repos = filter_repos_with_min_prs(repos, token, min_prs=100)
    print(f"Encontrados {len(filtered_repos)} repositórios com pelo menos 100 PRs.")

    # Salvar repositórios filtrados
    output_file = "data/selected_repos.csv"
    save_repos_to_csv(filtered_repos, output_file)


if __name__ == "__main__":
    import time

    main()