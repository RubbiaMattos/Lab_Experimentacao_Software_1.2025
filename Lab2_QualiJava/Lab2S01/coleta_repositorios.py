import os
import csv
import requests
import logging
from dotenv import load_dotenv

# 🌍 Configuração do ambiente
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.abspath(os.path.join(script_dir, "..", "..", ".env.config"))

if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    raise FileNotFoundError(f"❌ ERRO: O arquivo .env.config NÃO foi encontrado: {env_path}")

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise ValueError("❌ ERRO: Token GITHUB_TOKEN não foi encontrado no .env.config 🔑")

# 📂 Configuração de diretórios
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')

# 📝 Configuração do logger
# 🔹 Caminho relativo para salvar os logs
LOG_DIR = os.path.join(script_dir, "Relatórios")
LOG_FILE = os.path.join(LOG_DIR, "coleta_repositorios_log.log")

# 🔹 Criar diretório de logs, se não existir
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 🔹 Configuração do logger para salvar logs no arquivo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Exibe no console
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)

# 🔗 Configuração da API do GitHub
GITHUB_API_URL = "https://api.github.com/search/repositories"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def buscar_repositorios_mais_populares():
    """
    🌟 Consulta a API do GitHub e retorna os 1000 repositórios mais populares em Java.
    """
    logging.info("🚀 Buscando os 1000 repositórios mais populares em Java...")
    repositorios = []

    query_params = {
        "q": "language:Java",
        "sort": "stars",
        "order": "desc",
        "per_page": 100
    }

    # 🔄 Itera por até 10 páginas para obter até 1000 repositórios
    for page in range(1, 11):
        query_params["page"] = page
        logging.info(f"📄 Consultando a página {page} da API do GitHub...")
        response = requests.get(GITHUB_API_URL, headers=HEADERS, params=query_params)

        if response.status_code != 200:
            logging.error(f"❌ Erro ao consultar a API: {response.status_code} - {response.json().get('message')}")
            break

        data = response.json()
        items = data.get('items', [])

        for repo in items:
            repositorios.append((repo['clone_url'], repo['created_at']))

        if len(items) < 100:
            logging.info("📉 Menos de 100 repositórios retornados, encerrando a busca.")
            break

    logging.info(f"✅ Total de repositórios coletados: {len(repositorios)}")
    return repositorios

def salvar_repositorios_list_csv(repos):
    """
    💾 Salva a lista de URLs de repositórios no arquivo 'repositorios_list.csv'.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        with open(REPOS_LIST_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["clone_url", "created_at"])
            for repo_url, created_at in repos:
                writer.writerow([repo_url, created_at])
        logging.info(f"📥 Arquivo '{REPOS_LIST_FILE}' atualizado com {len(repos)} repositórios.")
    except Exception as e:
        logging.error(f"❌ Erro ao salvar os repositórios no CSV: {e}")
        raise

def main():
    logging.info("🚀 Iniciando coleta de repositórios...")
    repositorios = buscar_repositorios_mais_populares()
    if repositorios:
        salvar_repositorios_list_csv(repositorios)
        logging.info("🎉 Processo finalizado com sucesso! Repositórios salvos.")
    else:
        logging.warning("⚠️ Nenhum repositório foi coletado.")

if __name__ == "__main__":
    main()
