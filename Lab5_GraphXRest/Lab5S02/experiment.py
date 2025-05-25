#!/usr/bin/env python3
import time
import csv
import requests
import argparse

# --------------------------------------------------------------------
# Configuração: token embutido (hard-coded) – ATENÇÃO: não é a melhor prática
# --------------------------------------------------------------------
GITHUB_TOKEN = "GITHUB_TOKEN AQUI"

HEADERS_REST = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
HEADERS_GRAPHQL = {
    "Authorization": f"bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github.v4+json"
}

REST_URL_TEMPLATE = "https://api.github.com/repos/{owner}/{repo}"
GRAPHQL_URL = "https://api.github.com/graphql"

def measure_rest(owner: str, repo: str):
    start = time.time()
    url = REST_URL_TEMPLATE.format(owner=owner, repo=repo)
    resp = requests.get(url, headers=HEADERS_REST)
    resp.raise_for_status()
    return time.time() - start, len(resp.content)

def measure_graphql(owner: str, repo: str):
    query = """
    query($owner:String!, $repo:String!) {
      repository(owner:$owner, name:$repo) {
        issues(first:100) {
          totalCount
        }
      }
    }
    """
    payload = {"query": query, "variables": {"owner": owner, "repo": repo}}
    start = time.time()
    resp = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS_GRAPHQL)
    resp.raise_for_status()
    return time.time() - start, len(resp.content)

def run_experiment(owner: str, repo: str, trials: int):
    with open("experiment_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["API_Type", "Trial", "Response_Time", "Response_Size"])
        for i in range(1, trials + 1):
            rest_t, rest_s = measure_rest(owner, repo)
            writer.writerow(["REST", i, rest_t, rest_s])
            gql_t, gql_s = measure_graphql(owner, repo)
            writer.writerow(["GraphQL", i, gql_t, gql_s])
    print(f"✅ Experimento concluído ({trials} trials). Dados em 'experiment_results.csv'.")

# -------------------------------------------------
# Valores padrão – ajuste para o seu repositório
# -------------------------------------------------
DEFAULT_OWNER  = "RubbiaMattos"
DEFAULT_REPO   = "Lab_Experimentacao_Software_1.2025"
DEFAULT_TRIALS = 30

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compara performance REST vs GraphQL na GitHub API"
    )
    parser.add_argument(
        "--owner",
        default=DEFAULT_OWNER,
        help="Usuário/organização do repositório (padrão: %(default)s)"
    )
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help="Nome do repositório (padrão: %(default)s)"
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=DEFAULT_TRIALS,
        help="Número de medições (padrão: %(default)s)"
    )
    args = parser.parse_args()
    run_experiment(args.owner, args.repo, args.trials)
