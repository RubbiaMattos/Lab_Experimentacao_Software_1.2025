import time
import csv
import requests
import argparse
import sys
import logging
import json
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..",)))
from config_token import configurar_token

GITHUB_TOKEN = configurar_token()[0]

LOG_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(LOG_DIR, "experiment_incremental.log")
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

HEADERS_GRAPHQL = {
    "Authorization": f"bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github.v4+json"
}

GRAPHQL_URL = "https://api.github.com/graphql"

FIELDS_LEVELS = {
    "1campos": "name",
    "2campos": "name createdAt",
    "3campos": "name createdAt updatedAt",
    "4campos": "name createdAt updatedAt stargazerCount",
    "5campos": "name createdAt updatedAt stargazerCount forkCount",
    "6campos": "name createdAt updatedAt stargazerCount forkCount watchers { totalCount }",
    "7campos": "name createdAt updatedAt stargazerCount forkCount watchers { totalCount } issues { totalCount }",
    "8campos": "name createdAt updatedAt stargazerCount forkCount watchers { totalCount } issues { totalCount } pullRequests { totalCount }",
    "9campos": "name createdAt updatedAt stargazerCount forkCount watchers { totalCount } issues { totalCount } pullRequests { totalCount } languages(first: 5) { edges { size node { name } } }",
    "10campos": "name createdAt updatedAt stargazerCount forkCount watchers { totalCount } issues { totalCount } pullRequests { totalCount } languages(first: 5) { edges { size node { name } } } repositoryTopics(first: 5) { nodes { topic { name } } }"
}

def save_response_json(data, filename):
    resposta_dir = os.path.join(LOG_DIR, "respostas_incremental")
    os.makedirs(resposta_dir, exist_ok=True)
    full_path = os.path.join(resposta_dir, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Resposta salva em: {full_path}")

def measure_graphql_incremental(owner: str, repo: str, trial_name: str, fields: str, save_json=False):
    logger.info(f"\nIniciando chamada GraphQL ({trial_name}) com campos: {fields}")
    query = f"""
    query($owner:String!, $repo:String!) {{
      repository(owner:$owner, name:$repo) {{
        {fields}
      }}
    }}
    """
    payload = {"query": query, "variables": {"owner": owner, "repo": repo}}
    start = time.time()
    resp = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS_GRAPHQL)
    resp.raise_for_status()
    elapsed = time.time() - start
    size = len(resp.content)
    if save_json:
        save_response_json(resp.json(), f"graphql_response_{trial_name}.json")
    logger.info(f"{trial_name} - Tempo: {elapsed:.4f}s - Tamanho: {size} bytes")
    return elapsed, size

def run_incremental_experiment(owner: str, repo: str, trials: int):
    logger.info(f"Iniciando experimento incremental com {trials} execuções por nível de campos.")
    RESULTS_FILE = os.path.join(LOG_DIR, "experiment_graphql_incremental.csv")
    with open(RESULTS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Trial_Name", "Fields_Count", "Trial", "Response_Time", "Response_Size"])
        for level_name, fields in FIELDS_LEVELS.items():
            for i in range(1, trials + 1):
                logger.info(f"\nTrial {i}/{trials} - Campos: {level_name}")
                save_json_flag = (i == 1)
                time_taken, size = measure_graphql_incremental(owner, repo, level_name, fields, save_json=save_json_flag)
                writer.writerow([level_name, len(fields.split()), i, time_taken, size])
    logger.info("\n✅ Experimento incremental concluído.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", default="RubbiaMattos")
    parser.add_argument("--repo", default="Lab_Experimentacao_Software_1.2025")
    parser.add_argument("--trials", type=int, default=30)
    args = parser.parse_args()
    run_incremental_experiment(args.owner, args.repo, args.trials)