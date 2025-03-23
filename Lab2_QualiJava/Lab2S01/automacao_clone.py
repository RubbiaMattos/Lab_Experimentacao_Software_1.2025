import os
import csv
import subprocess
import logging
import psutil
import shutil
import stat
from dotenv import load_dotenv
import time

# 📄 Carregando variáveis de ambiente
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.abspath(os.path.join(script_dir, "..", "..", ".env.config"))

if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    raise FileNotFoundError(f"❌ ERRO: O arquivo .env.config NÃO foi encontrado: {env_path}")

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise ValueError("❌ ERRO: Token GITHUB_TOKEN não foi encontrado no .env.config 🔐")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'Data')
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')

REPOS_DIR = os.path.join(BASE_DIR, 'Repos')
LOG_DIR = os.path.join(BASE_DIR, "Relatórios")
LOG_FILE = os.path.join(LOG_DIR, "automacao_clone.log")
os.makedirs(LOG_DIR, exist_ok=True)

# ✅ Configuração do LOG sem o nível (INFO/WARNING) pra manter alinhado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE, encoding="utf-8")]
)

log_info = logging.info
log_warning = logging.warning
log_error = logging.error

MEMORY_THRESHOLD_MB = 500
DISK_THRESHOLD_MB = 1024
MAX_RETRIES = 5

def recursos_suficientes():
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage(REPOS_DIR)
    if mem.available / (1024 * 1024) < MEMORY_THRESHOLD_MB:
        logging.error("🛑 Memória insuficiente")
        return False
    if disk.free / (1024 * 1024) < DISK_THRESHOLD_MB:
        logging.error("🛑 Espaço em disco insuficiente")
        return False
    return True

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def repositorio_clonado_completo(repo_path):
    return os.path.isdir(os.path.join(repo_path, '.git'))

def fetch_and_compare(repo_path):
    try:
        subprocess.run(['git', '-C', repo_path, 'fetch'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        branch = subprocess.check_output(['git', '-C', repo_path, 'rev-parse', '--abbrev-ref', 'HEAD'], stderr=subprocess.DEVNULL).strip().decode()
        remote_commit = subprocess.check_output(['git', '-C', repo_path, 'rev-parse', f'origin/{branch}'], stderr=subprocess.DEVNULL).strip()
        local_commit = subprocess.check_output(['git', '-C', repo_path, 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL).strip()
        return local_commit == remote_commit
    except subprocess.CalledProcessError:
        return False

def clonar_repositorios():
    if not os.path.exists(REPOS_LIST_FILE):
        raise FileNotFoundError(f"📄 Lista de repositórios não encontrada: {REPOS_LIST_FILE}")

    os.makedirs(REPOS_DIR, exist_ok=True)
    with open(REPOS_LIST_FILE, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        repositorios = list(csv_reader)

    total_repos = len(repositorios)
    cloned_count = 0

    for idx, row in enumerate(repositorios, start=1):
        if not row:
            continue

        repo_url = row[0].strip()
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(REPOS_DIR, repo_name)

        idx_display = f"{idx:02}"
        log_prefix = f"({idx_display}/{total_repos})"
        padding = ' ' * len(log_prefix)

        logging.info(f"{log_prefix} 📂 Processando: \033[33m{repo_name}\033[0m")

        if os.path.exists(repo_path):
            logging.info(f"{padding} 🔎 Verificando se o repositório \033[35m{repo_name}\033[0m está atualizado...")
            if repositorio_clonado_completo(repo_path) and fetch_and_compare(repo_path):
                logging.info(f"{padding} ✅ \033[35m{repo_name}\033[0m está atualizado e não será re-clonado.")
                continue
            else:
                logging.warning(f"{padding} ⚠️ \033[35m{repo_name}\033[0m está incompleto ou desatualizado. Excluindo e re-clonando...")
                shutil.rmtree(repo_path, onerror=remove_readonly)

        if not recursos_suficientes():
            logging.error(f"{padding} 🛑 Recursos insuficientes! Encerrando... ({idx_display}/{total_repos})")
            break

        attempt = 0
        success = False
        while attempt < MAX_RETRIES:
            try:
                logging.info(f"{padding} 🔄 Clonando \033[35m{repo_name}\033[0m...")
                subprocess.run(['git', 'clone', repo_url, repo_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                logging.info(f"{padding} 🔍 Comparando repositório local e remoto após a clonagem...")
                success = fetch_and_compare(repo_path)
                if success:
                    break
                else:
                    logging.warning(f"{padding} ⚠️ Repositório clonado incompleto, tentando novamente...")
                    shutil.rmtree(repo_path, onerror=remove_readonly)
            except subprocess.CalledProcessError:
                attempt += 1
                logging.warning(f"{padding} ⚠️ Erro ao clonar, tentativa {attempt}/{MAX_RETRIES}")
                time.sleep(5)

        if not success:
            logging.error(f"{padding} ❌ Falha ao clonar \033[35m{repo_name}\033[0m após {MAX_RETRIES} tentativas.")
        else:
            cloned_count += 1
            logging.info(f"{padding} ✅ Clonado com sucesso: \033[35m{repo_name}\033[0m (Total: {cloned_count})")

    logging.info(f"🎯 Clonagem finalizada! Total clonado: {cloned_count} de {total_repos}")

def contar_repositorios_clonados():
    if not os.path.exists(REPOS_DIR):
        logging.error(f"❌ Diretório não encontrado: {REPOS_DIR}")
        return 0

    total = 0
    for pasta in os.listdir(REPOS_DIR):
        repo_path = os.path.join(REPOS_DIR, pasta)
        if os.path.isdir(repo_path) and os.path.isdir(os.path.join(repo_path, '.git')):
            total += 1
        else:
            logging.warning(f"⚠️ Repositório inválido ou incompleto: {pasta}")

    logging.info(f"📈 Total de repositórios clonados na pasta: {total}")

    if total < 1000:
        logging.warning(f"⚠️ Apenas {total} repositórios encontrados. Esperado: 1000")
    elif total > 1000:
        logging.warning(f"⚠️ Atenção! {total} repositórios encontrados, mais que o esperado.")
    else:
        logging.info(f"✅ Todos os 1000 repositórios clonados com sucesso!")

    return total

if __name__ == "__main__":
    logging.info("🚀 Iniciando o processo de clonagem dos repositórios...\n")
    clonar_repositorios()
    total_clonados = contar_repositorios_clonados()

    if total_clonados == 1000:
        logging.info("🎉 Quantidade correta de repositórios clonados! Pronto para a próxima etapa.")
    else:
        logging.error(f"❌ Foram encontrados {total_clonados} repositórios. Esperado: 1000. Verifique! 📌")