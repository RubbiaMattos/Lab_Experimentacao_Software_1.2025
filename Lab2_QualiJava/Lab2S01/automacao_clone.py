import os
import csv
import subprocess
import logging
import time
from dotenv import load_dotenv

# 🔹 Diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))

# 🔹 Subir um nível para tentar encontrar o Lab1_RepoPop
repo_root = os.path.abspath(os.path.join(script_dir, ".."))

# 🔹 Caminho dinâmico do .env.config
env_path = os.path.join(repo_root, ".env.config")

# 🔹 Imprimir caminhos para depuração
print(f"📌 Diretório do script: {script_dir}")
print(f"📌 Diretório esperado do repositório: {repo_root}")
print(f"📌 Caminho esperado do .env.config: {env_path}")

# 🔹 Verificar se o arquivo existe antes de carregar
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Arquivo .env.config carregado de: {env_path}")
else:
    raise FileNotFoundError(f"❌ ERRO: O arquivo .env.config NÃO foi encontrado no caminho esperado: {env_path}")

# 🔹 Testar se o token foi carregado corretamente
TOKEN = os.getenv("GITHUB_TOKEN")

if TOKEN:
    print("✅ Token carregado com sucesso!")
else:
    raise ValueError("❌ ERRO: Token GITHUB_TOKEN não foi encontrado no .env.config.")

# Configuração de diretórios
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPOS_DIR = os.path.join(DATA_DIR, 'repos')  # Diretório onde os repositórios serão clonados
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')  # CSV com as URLs dos repositórios

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def configurar_git():
    """
    Configura o Git para evitar erros de transferência e aumentar a estabilidade.
    """
    try:
        subprocess.run(['git', 'config', '--global', 'http.postBuffer', '100M'], check=True)
        subprocess.run(['git', 'config', '--global', 'http.version', 'HTTP/1.1'], check=True)
        subprocess.run(['git', 'config', '--global', 'core.compression', '0'], check=True)
        subprocess.run(['git', 'config', '--global', 'core.longpaths', 'true'], check=True)
        subprocess.run(['git', 'config', '--global', 'core.ignorecase', 'false'], check=True)
        subprocess.run(['git', 'config', '--global', 'pack.windowMemory', '256m'], check=True)
        subprocess.run(['git', 'config', '--global', 'pack.packSizeLimit', '256m'], check=True)
        subprocess.run(['git', 'config', '--global', 'pack.threads', '1'], check=True)
        logging.info("✅ Configurações do Git atualizadas!")
    except subprocess.CalledProcessError as e:
        logging.error("❌ Falha ao configurar o Git: " + str(e))

def clonar_repositorio(repo_url, repo_path, tentativas=3):
    """
    Tenta clonar um repositório até um número máximo de tentativas.
    Usa `--filter=blob:none` e `--single-branch` para reduzir a quantidade de dados transferidos.
    """
    for tentativa in range(tentativas):
        try:
            logging.info(f"🔹 Tentativa {tentativa+1}/{tentativas} - Clonando: {repo_url}")
            subprocess.run([
                'git', 'clone', '--depth=1', '--filter=blob:none', '--single-branch',
                repo_url, repo_path
            ], check=True)

            # Opcional: usar sparse-checkout para baixar apenas pastas específicas
            sparse_dirs = ['src', 'docs']  # Defina as pastas que deseja baixar
            if sparse_dirs:
                os.chdir(repo_path)
                subprocess.run(['git', 'sparse-checkout', 'init', '--cone'], check=True)
                subprocess.run(['git', 'sparse-checkout', 'set'] + sparse_dirs, check=True)
                os.chdir(script_dir)  # Volta ao diretório original
            
            logging.info(f"✅ Repositório clonado com sucesso: {repo_url}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"⚠️ Erro ao clonar {repo_url}: {e}")
            time.sleep(5)  # Aguarda antes de tentar novamente
    logging.error(f"🚨 Falha ao clonar {repo_url} após {tentativas} tentativas.")
    return False

def clonar_repositorios():
    """
    Clona os repositórios listados em repositorios_list.csv.
    Se o processo for interrompido, retoma clonando apenas os repositórios que ainda não foram clonados.
    """
    if not os.path.exists(REPOS_LIST_FILE):
        raise FileNotFoundError(f"Arquivo não encontrado: {REPOS_LIST_FILE}")

    if not os.path.exists(REPOS_DIR):
        os.makedirs(REPOS_DIR)

    with open(REPOS_LIST_FILE, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        repositorios = list(csv_reader)

    total_repos = len(repositorios)
    cloned_count = 0

    for idx, row in enumerate(repositorios, start=1):
        repo_url = row[0].strip()
        if not repo_url:
            continue

        # Extrai o nome do repositório a partir da URL (removendo ".git")
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(REPOS_DIR, repo_name)

        # Se o repositório já foi clonado (diretório existe e contém a pasta .git), pula para o próximo
        if os.path.exists(repo_path) and os.path.isdir(os.path.join(repo_path, '.git')):
            logging.info(f"({idx}/{total_repos}) Repositório já clonado: {repo_name}. Pulando...")
            continue

        if clonar_repositorio(repo_url, repo_path):
            cloned_count += 1

    logging.info(f"🎉 Processo de clonagem concluído. Total de repositórios clonados: {cloned_count} de {total_repos}")

def main():
    logging.info("🚀 Iniciando automação para clonagem de repositórios...")
    configurar_git()
    try:
        clonar_repositorios()
    except Exception as e:
        logging.error(f"❌ Erro geral no script: {e}")
        raise

if __name__ == "__main__":
    main()
