import os
import csv
import subprocess
import logging
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# 🔹 Diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(script_dir, ".."))  # Volta um nível

# 🔹 Caminho dinâmico do .env.config
env_path = os.path.join(repo_root, ".env.config")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Arquivo .env.config carregado de: {env_path}")
else:
    raise FileNotFoundError(f"❌ ERRO: O arquivo .env.config NÃO foi encontrado no caminho esperado: {env_path}")

# 🔹 Testar se o token foi carregado corretamente
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise ValueError("❌ ERRO: Token GITHUB_TOKEN não foi encontrado no .env.config.")

# Configuração de diretórios
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPOS_DIR = os.path.join(DATA_DIR, 'repos')  # Diretório onde os repositórios serão clonados
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')  # CSV com as URLs dos repositórios

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Criar diretórios caso não existam
os.makedirs(REPOS_DIR, exist_ok=True)

# Função para clonar um único repositório
def clonar_repositorio(repo_url, idx, total_repos):
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    repo_path = os.path.join(REPOS_DIR, repo_name)

    # Se o repositório já existe, pula para o próximo
    if os.path.exists(repo_path) and os.path.isdir(os.path.join(repo_path, '.git')):
        logging.info(f"({idx}/{total_repos}) Repositório já clonado: {repo_name}. Pulando...")
        return f"✔️ {repo_name} já existe"

    try:
        logging.info(f"({idx}/{total_repos}) Clonando repositório: {repo_url}")
        subprocess.run(['git', 'clone', '--depth=1', repo_url, repo_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"✅ {repo_name} clonado com sucesso!"
    except subprocess.CalledProcessError as e:
        return f"❌ Erro ao clonar {repo_name}: {e}"

# Função principal para gerenciar a clonagem paralela
def clonar_repositorios():
    if not os.path.exists(REPOS_LIST_FILE):
        raise FileNotFoundError(f"Arquivo não encontrado: {REPOS_LIST_FILE}")

    with open(REPOS_LIST_FILE, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        repositorios = [row[0].strip() for row in csv_reader if row]

    total_repos = len(repositorios)
    logging.info(f"Iniciando clonagem de {total_repos} repositórios...")

    # Usando ThreadPoolExecutor para clonar repositórios em paralelo
    max_workers = min(10, os.cpu_count())  # Define um número adequado de threads
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_repo = {executor.submit(clonar_repositorio, repo, idx, total_repos): repo for idx, repo in enumerate(repositorios, start=1)}
        for future in as_completed(future_to_repo):
            results.append(future.result())

    logging.info("Processo de clonagem concluído.")
    for result in results:
        logging.info(result)

# Função principal
def main():
    logging.info("🚀 Iniciando automação para clonagem de repositórios...")
    try:
        clonar_repositorios()
    except Exception as e:
        logging.error(f"Erro geral no script: {e}")

if __name__ == "__main__":
    main()
