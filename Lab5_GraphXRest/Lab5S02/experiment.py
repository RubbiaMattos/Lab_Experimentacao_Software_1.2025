import time
import csv
import requests
import argparse
import sys
import logging
import json
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from config_token import configurar_token

GITHUB_TOKEN = configurar_token()[0]

LOG_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(LOG_DIR, "experiment.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

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

def measure_rest(owner: str, repo: str, save_json=False):
    logger.info(f"Iniciando chamada REST para {owner}/{repo}")
    start = time.time()
    url = REST_URL_TEMPLATE.format(owner=owner, repo=repo)
    resp = requests.get(url, headers=HEADERS_REST)
    resp.raise_for_status()
    logger.info(f"Chamada REST concluída em {time.time() - start:.4f}s")

    if save_json:
        save_response_json(resp.json(), "rest_response.json")

    return time.time() - start, len(resp.content)

def measure_graphql(owner: str, repo: str, save_json=False):
    logger.info(f"Iniciando chamada GraphQL para {owner}/{repo}")
    query = """
    query($owner: String!, $repo: String!) {
      repository(owner: $owner, name: $repo) {
        name
        nameWithOwner
        description
        descriptionHTML
        shortDescriptionHTML(limit: 200)
        homepageUrl
        url
        resourcePath
        sshUrl
        createdAt
        updatedAt
        pushedAt
        visibility
        isPrivate
        diskUsage
        forkCount
        forks(first: 5) {
          totalCount
          nodes { nameWithOwner }
        }
        stargazerCount
        watchers {
          totalCount
        }
        issues {
          totalCount
        }
        pullRequests {
          totalCount
        }
        licenseInfo {
          key
          name
          url
        }
        languages(first: 5) {
          edges {
            size
            node {
              name
            }
          }
        }
        repositoryTopics(first: 5) {
          nodes {
            topic {
              name
            }
          }
        }
        defaultBranchRef {
          name
          prefix
        }
        primaryLanguage {
          name
        }
      }
    }
    """
    payload = {"query": query, "variables": {"owner": owner, "repo": repo}}

    start = time.time()
    resp = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS_GRAPHQL)
    resp.raise_for_status()
    duration = time.time() - start
    logger.info(f"Chamada GraphQL concluída em {duration:.4f}s")

    if save_json:
        save_response_json(resp.json(), "graphql_response.json")

    return duration, len(resp.content)

def save_response_json(data, filename):
    resposta_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "respostas_json")
    os.makedirs(resposta_dir, exist_ok=True)
    full_path = os.path.join(resposta_dir, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Resposta salva em: {full_path}")

def run_experiment(owner: str, repo: str, trials: int):
    logger.info(f"Iniciando experimento com {trials} execuções para {owner}/{repo}")
    RESULTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "experiment_results.csv")
    with open(RESULTS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["API_Type", "Trial", "Response_Time", "Response_Size"])
        for i in range(1, trials + 1):
            logger.info(f"Execução {i}/{trials}")
            save_json_flag = (i == 1)
            rest_t, rest_s = measure_rest(owner, repo, save_json=save_json_flag)
            writer.writerow(["REST", i, rest_t, rest_s])
            gql_t, gql_s = measure_graphql(owner, repo, save_json=save_json_flag)
            writer.writerow(["GraphQL", i, gql_t, gql_s])
    logger.info("Experimento concluído com sucesso.")
    print(f"✅ Experimento concluído ({trials} trials). Dados em 'experiment_results.csv'.")

# -------------------------------------------------
# Valores padrão
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
