import os
import csv
import requests
import logging
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.abspath(os.path.join(script_dir, "..", "..", ".env.config"))

if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    raise FileNotFoundError(f"❌ ERRO: O arquivo .env.config NÃO foi encontrado: {env_path}")

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise ValueError("❌ ERRO: Token GITHUB_TOKEN não foi encontrado no .env.config")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')
GITHUB_API_URL = "https://api.github.com/search/repositories"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def buscar_repositorios_mais_populares():
    logging.info("🔎 Buscando os 1000 repositórios mais populares em Java...")
    repositorios = []

    query_params = {
        "q": "language:Java",
        "sort": "stars",
        "order": "desc",
        "per_page": 100
    }

    for page in range(1, 11):
        query_params["page"] = page
        logging.info(f"📄 Consultando a página {page}...")
        response = requests.get(GITHUB_API_URL, headers=HEADERS, params=query_params)
        if response.status_code != 200:
            logging.error(f"❌ Erro na API: {response.status_code} - {response.json().get('message')}")
            break
        data = response.json()
        items = data.get('items', [])
        for repo in items:
            repositorios.append([
                repo['clone_url'],
                repo['stargazers_count'],
                repo['created_at'],
                repo['pushed_at'],
                repo['releases_url'].replace('{/id}', '')
            ])
        if len(items) < 100:
            break

    logging.info(f"✅ Total de repositórios coletados: {len(repositorios)}")
    return repositorios

def salvar_repositorios_list_csv(repos):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(REPOS_LIST_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["clone_url", "stars", "created_at", "last_push", "releases_url"])
        writer.writerows(repos)
    logging.info(f"💾 Arquivo '{REPOS_LIST_FILE}' atualizado com {len(repos)} repositórios.")

def main():
    logging.info("🚀 Iniciando coleta de repositórios...")
    repositorios = buscar_repositorios_mais_populares()
    if repositorios:
        salvar_repositorios_list_csv(repositorios)
    else:
        logging.warning("⚠️ Nenhum repositório foi coletado.")

if __name__ == "__main__":
    main()
