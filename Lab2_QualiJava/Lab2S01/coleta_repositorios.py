import os
import csv
import requests
import logging
from dotenv import load_dotenv

# Configuração do ambiente e logger
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.abspath(os.path.join(script_dir, "..", "..", ".env.config"))

if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    raise FileNotFoundError(f"❌ ERRO: O arquivo .env.config NÃO foi encontrado: {env_path}")

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise ValueError("❌ ERRO: Token GITHUB_TOKEN não foi encontrado no .env.config 🔑")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')

LOG_DIR = os.path.join(script_dir, "Relatórios")
LOG_FILE = os.path.join(LOG_DIR, "coleta_repositorios_log.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE, encoding="utf-8")]
)

GITHUB_API_URL = "https://api.github.com/search/repositories"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def buscar_repositorios_open_source():
    logging.info("===== 🌐 BUSCANDO REPOSITÓRIOS OPEN SOURCE =====")
    repositorios = []

    query_params = {
        "q": "language:Java license:mit license:apache license:gpl license:bsd",
        "sort": "stars",
        "order": "desc",
        "per_page": 100
    }

    for page in range(1, 11):
        query_params["page"] = page
        logging.info(f"📄 Consultando página {page}/10 da API do GitHub...")
        response = requests.get(GITHUB_API_URL, headers=HEADERS, params=query_params)

        if response.status_code != 200:
            logging.error(f"❌ Erro na API (Status {response.status_code}): {response.json().get('message')}")
            break

        data = response.json()
        items = data.get('items', [])

        for repo in items:
            repositorios.append((repo['clone_url'], repo['created_at']))

        if len(items) < 100:
            logging.info("📉 Menos de 100 resultados obtidos, encerrando busca antecipadamente.")
            break

    logging.info(f"✅ Busca concluída: {len(repositorios)} repositórios coletados.")
    return repositorios

def salvar_repositorios_list_csv(repos):
    logging.info("💾 Salvando lista de repositórios em CSV...")
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        with open(REPOS_LIST_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["clone_url", "created_at"])
            for repo_url, created_at in repos:
                writer.writerow([repo_url, created_at])
        logging.info(f"✅ CSV salvo com sucesso em '{REPOS_LIST_FILE}' ({len(repos)} registros).")
    except Exception as e:
        logging.error(f"❌ Falha ao salvar CSV: {e}")
        raise

def main():
    repositorios = buscar_repositorios_open_source()
    if repositorios:
        salvar_repositorios_list_csv(repositorios)
        logging.info("🎉 Coleta de repositórios concluída com sucesso!")
    else:
        logging.warning("⚠️ Nenhum repositório foi coletado.")

if __name__ == "__main__":
    main()
