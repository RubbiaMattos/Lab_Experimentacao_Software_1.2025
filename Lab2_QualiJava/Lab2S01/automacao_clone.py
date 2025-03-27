import os
import csv
import subprocess
import logging
import psutil
import shutil
import stat
import time
from config_token import configurar_token

TOKEN = configurar_token()

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
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
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
        branch = subprocess.check_output(['git', '-C', repo_path, 'symbolic-ref', '--short', 'HEAD']).strip().decode()
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
        next(csv_reader, None)  # Pula cabeçalho
        repositorios_raw = [row for row in csv_reader if row]

    total_repos = len(repositorios_raw)
    cloned_count = 0

    for idx, row in enumerate(repositorios_raw, start=1):
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
                shutil.rmtree(repo_path, onexc=remove_readonly)

        if not recursos_suficientes():
            logging.error(f"{padding} 🛑 Recursos insuficientes! Encerrando... ({idx_display}/{total_repos})")
            break

        attempt = 0
        success = False
        while attempt < MAX_RETRIES:
            try:
                logging.info(f"{padding} 🔄 Clonando {repo_name}...")
                result = subprocess.run(['git', 'clone', repo_url, repo_path], capture_output=True, text=True)
                
                if result.returncode != 0:
                    logging.error(f"{padding} ❌ Erro ao clonar {repo_name}: {result.stderr.strip()}")
                    attempt += 1
                    time.sleep(5)
                    continue
                time.sleep(10)

                if not os.path.exists(os.path.join(repo_path, '.git')):
                    logging.warning(f"{padding} ⚠️ {repo_name} clonado mas .git não encontrado. Tentando novamente...")
                    shutil.rmtree(repo_path, onexc=remove_readonly)
                    attempt += 1
                    time.sleep(5)
                    continue

                # Se chegou aqui, clone foi bem-sucedido
                success = True
                break

            except subprocess.CalledProcessError:
                attempt += 1
                logging.warning(f"{padding} ⚠️ Erro ao clonar, tentativa {attempt}/{MAX_RETRIES}")
                time.sleep(10)

        if not success:
            logging.error(f"{padding} ❌ Falha ao clonar \033[35m{repo_name}\033[0m após {MAX_RETRIES} tentativas.")
        else:
            cloned_count += 1
            logging.info(f"{padding} ✅ Clonado com sucesso: \033[35m{repo_name}\033[0m (Total: {cloned_count})")

def contar_repositorios_clonados():
    if not os.path.exists(REPOS_DIR):
        logging.error(f"❌ Diretório não encontrado: {REPOS_DIR}")
        return 0

    total = 0
    for pasta in os.listdir(REPOS_DIR):
        repo_path = os.path.join(REPOS_DIR, pasta)
        if os.path.isdir(repo_path):
            if os.path.isdir(os.path.join(repo_path, '.git')):
                total += 1
            else:
                logging.warning(f"⚠️ Pasta {pasta} está presente mas o .git está faltando (clone pode ter falhado)")

    logging.info(f"📈 Total de repositórios clonados na pasta: {total}")

    if total < 1000:
        logging.warning(f"⚠️ Apenas {total} repositórios encontrados. Esperado: 1000")
    elif total > 1000:
        logging.warning(f"⚠️ Atenção! {total} repositórios encontrados, mais que o esperado.")
    else:
        logging.info(f"✅ Todos os 1000 repositórios clonados com sucesso!")

    return total


def verificar_pastas_inconsistentes():
    if not os.path.exists(REPOS_LIST_FILE):
        logging.error(f"❌ Lista de repositórios não encontrada: {REPOS_LIST_FILE}")
        return []

    with open(REPOS_LIST_FILE, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)  # Pula o cabeçalho
        repositorios_raw = [row for row in csv_reader if row]

    # Extrai o nome do repositório da URL
    repositorios_listados = [row[0].strip().split('/')[-1].replace('.git', '') for row in repositorios_raw]
    repo_url_mapping = {row[0].strip().split('/')[-1].replace('.git', ''): row[0].strip() for row in repositorios_raw}

    # Repositórios presentes no disco
    pastas_no_disco = {pasta for pasta in os.listdir(REPOS_DIR) if os.path.isdir(os.path.join(REPOS_DIR, pasta, '.git'))}
    pastas_esperadas = set(repositorios_listados)

    # Pastas a mais
    pastas_extras = pastas_no_disco - pastas_esperadas
    if pastas_extras:
        logging.warning("⚠️ Pastas que estão na pasta 'Repos' mas NÃO estão na lista de repositórios esperados:")
        for pasta in sorted(pastas_extras):
            logging.warning(f"   - {pasta}")
    else:
        logging.info("✅ Nenhuma pasta extra encontrada na pasta 'Repos'.")

    # Pastas faltando
    pastas_faltando = pastas_esperadas - pastas_no_disco
    if pastas_faltando:
        logging.warning("⚠️ Repositórios listados que NÃO estão presentes na pasta 'Repos':")
        for pasta in sorted(pastas_faltando):
            logging.warning(f"   - {pasta}")
        return list(pastas_faltando)  # Retorna os faltantes
    else:
        logging.info("✅ Nenhuma pasta faltando. Todas as listadas foram encontradas na pasta 'Repos'.")
        return []

def clonar_faltantes(faltantes):
    with open(REPOS_LIST_FILE, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)  # pula cabeçalho
        repo_urls = {row[0].strip().split('/')[-1].replace('.git', ''): row[0].strip() for row in csv_reader if row}

    for repo_name in faltantes:
        repo_url = repo_urls.get(repo_name)
        if not repo_url:
            logging.error(f"❌ URL do repositório {repo_name} não encontrada na lista.")
            continue

        repo_path = os.path.join(REPOS_DIR, repo_name)
        logging.info(f"🔄 Re-clonando faltante: {repo_name}...")
        result = subprocess.run(['git', 'clone', repo_url, repo_path], capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"❌ Erro ao clonar {repo_name}: {result.stderr.strip()}")
        else:
            logging.info(f"✅ Repositório {repo_name} clonado com sucesso.")


if __name__ == "__main__":
    logging.info("🚀 Iniciando o processo de clonagem dos repositórios...\n")

    # Etapa 1 - Clonagem inicial
    clonar_repositorios()

    # Etapa 2 - Verifica se há repositórios faltantes
    logging.info("\n🔎 Verificando inconsistências e repositórios faltantes...")
    faltantes = verificar_pastas_inconsistentes()

    # Etapa 3 - Tenta clonar os faltantes (se houver)
    if faltantes:
        logging.info(f"🔄 Tentando clonar os repositórios faltantes ({len(faltantes)} repositórios)...")
        clonar_faltantes(faltantes)
    else:
        logging.info("✅ Nenhum repositório faltante. Tudo certo até aqui!")

    # Etapa 4 - Contagem final
    total_clonados = contar_repositorios_clonados()

    # Etapa 5 - Validação final
    if total_clonados == 1000:
        logging.info("🎉 Quantidade correta de repositórios clonados! Processo concluído com sucesso.")
    else:
        logging.error(f"❌ Foram encontrados {total_clonados} repositórios. Esperado: 1000. Verifique! 📌")