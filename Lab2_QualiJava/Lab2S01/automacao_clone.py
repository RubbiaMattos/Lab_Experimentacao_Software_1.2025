import os
import csv
import subprocess
import logging
import re
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
REPOS_DIR = os.path.join(BASE_DIR, 'repos')
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
GIT_URL_PATTERN = re.compile(r'^https://.+\\.git$')
ALLOWED_DOMAINS = ["github.com", "gitlab.com"]

def clonar_repositorios():
    if not os.path.exists(REPOS_LIST_FILE):
        raise FileNotFoundError(f"❌ Arquivo não encontrado: {REPOS_LIST_FILE}")
    os.makedirs(REPOS_DIR, exist_ok=True)

    with open(REPOS_LIST_FILE, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        repositorios = list(csv_reader)

    total_repos = len(repositorios)
    cloned_count = 0

    for idx, row in enumerate(repositorios, start=1):
        repo_url = row['clone_url'].strip()
        if not repo_url or not GIT_URL_PATTERN.match(repo_url) or not any(domain in repo_url for domain in ALLOWED_DOMAINS):
            logging.info(f"⚠️ ({idx}/{total_repos}) URL inválida ou domínio não permitido. Pulando...")
            continue

        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(REPOS_DIR, repo_name)

        if os.path.exists(repo_path) and os.path.isdir(os.path.join(repo_path, '.git')):
            logging.info(f"✔️ ({idx}/{total_repos}) Repositório já clonado: {repo_name}. Pulando...")
            continue

        try:
            logging.info(f"⏳ ({idx}/{total_repos}) Clonando repositório: {repo_url}")
            subprocess.run(['git', 'clone', '--depth', '1', repo_url, repo_path], check=True)
            cloned_count += 1
            logging.info(f"✅ Repositório clonado com sucesso: {repo_name} (Total clonado: {cloned_count})")
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Erro ao clonar repositório '{repo_url}': {e}")

    logging.info(f"🏁 Processo de clonagem concluído. Total de repositórios clonados: {cloned_count} de {total_repos}")

def main():
    logging.info("🚀 Iniciando automação para clonagem de repositórios...")
    try:
        clonar_repositorios()
    except Exception as e:
        logging.error(f"❌ Erro geral no script: {e}")
        raise

if __name__ == "__main__":
    main()
