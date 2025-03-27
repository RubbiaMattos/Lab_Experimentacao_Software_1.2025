import os
import csv
import requests
import logging
from config_token import configurar_token

TOKEN = configurar_token()
# Configuração do ambiente e logger
script_dir = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')

LOG_DIR = os.path.join(script_dir, "Relatórios")
LOG_FILE = os.path.join(LOG_DIR, "coleta_repositorios.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)

GITHUB_API_URL = "https://api.github.com/search/repositories"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def get_releases_count(repo_full_name):
    """
    📈 Obtém o número de releases do repositório.
    """
    releases_url = f"https://api.github.com/repos/{repo_full_name}/releases"
    response = requests.get(releases_url, headers=HEADERS)
    
    if response.status_code == 200:
        return len(response.json())
    else:
        logging.warning(f"⚠️ Não foi possível obter releases para {repo_full_name}: {response.status_code}")
        return 0

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
            repo_full_name = repo['full_name']
            releases_count = get_releases_count(repo_full_name)
            repositorios.append((repo['clone_url'], repo['created_at'], repo['stargazers_count'], releases_count))

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
            output_dir = DATA_DIR
            relative_output_dir = os.path.relpath(output_dir, BASE_DIR)
            writer = csv.writer(csv_file)
            writer.writerow(["clone_url", "created_at", "stars", "releases"])
            for repo_url, created_at, stars, releases in repos:
                writer.writerow([repo_url, created_at, stars, releases])
        logging.info(f"✅ CSV salvo com sucesso em '{relative_output_dir}' ({len(repos)} registros).")
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
