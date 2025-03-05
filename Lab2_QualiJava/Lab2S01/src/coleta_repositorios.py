import os
import csv
import requests
import logging
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()

# Configuração de diretórios
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuração da API do GitHub
GITHUB_API_URL = "https://api.github.com/search/repositories"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("Você precisa configurar o GITHUB_TOKEN no arquivo .env.")
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}


def buscar_repositorios_mais_populares():
    """
    Consulta a API do GitHub e retorna os 1000 repositórios mais populares em Java.
    """
    logging.info("Buscando os 1000 repositórios mais populares em Java...")
    repositorios = []

    # Parâmetros de consulta: filtra por repositórios Java, ordenados por estrelas
    query_params = {
        "q": "language:Java",
        "sort": "stars",
        "order": "desc",
        "per_page": 100
    }

    # Itera por até 10 páginas para obter até 1000 repositórios
    for page in range(1, 11):
        query_params["page"] = page
        logging.info(f"Consultando a página {page}...")
        response = requests.get(GITHUB_API_URL, headers=HEADERS, params=query_params)
        if response.status_code != 200:
            logging.error(f"Erro ao consultar a API: {response.status_code} - {response.json().get('message')}")
            break
        data = response.json()
        items = data.get('items', [])
        for repo in items:
            repositorios.append(repo['clone_url'])
        if len(items) < 100:
            break

    logging.info(f"Total de repositórios coletados: {len(repositorios)}")
    return repositorios


def salvar_repositorios_list_csv(repos):
    """
    Salva a lista de URLs de repositórios no arquivo 'repositorios_list.csv'.
    """
    # Certifica-se de que a pasta DATA_DIR exista
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        with open(REPOS_LIST_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            for repo_url in repos:
                writer.writerow([repo_url])
        logging.info(f"Arquivo '{REPOS_LIST_FILE}' atualizado com {len(repos)} repositórios.")
    except Exception as e:
        logging.error(f"Erro ao salvar os repositórios no CSV: {e}")
        raise


def main():
    logging.info("Iniciando coleta de repositórios...")
    repositorios = buscar_repositorios_mais_populares()
    if repositorios:
        salvar_repositorios_list_csv(repositorios)
    else:
        logging.warning("Nenhum repositório foi coletado.")


if __name__ == "__main__":
    main()
