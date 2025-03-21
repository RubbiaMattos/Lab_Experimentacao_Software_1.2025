import os
import subprocess
import pandas as pd
import logging
import time
from datetime import datetime
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.abspath(os.path.join(script_dir, "..", "..", ".env.config"))

if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    raise FileNotFoundError(f"❌ ERRO: Arquivo .env.config NÃO encontrado: {env_path}")

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise ValueError("❌ ERRO: Token GITHUB_TOKEN não encontrado no .env.config 🔑")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPOS_DIR = os.path.join(DATA_DIR, 'C:\\Repos')
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')
CK_JAR = os.path.join(BASE_DIR, 'ck.jar')

LOG_DIR = os.path.join(script_dir, "Relatórios")
LOG_FILE = os.path.join(LOG_DIR, "coletar_dados_log.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE, encoding="utf-8")]
)

CK_TIMEOUT = 300

def formatar_tempo(segundos):
    horas, resto = divmod(int(segundos), 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def run_ck(repo_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    command = ['java', '-jar', CK_JAR, repo_path, "true", "0", "true", output_dir]
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=CK_TIMEOUT)
    except subprocess.TimeoutExpired:
        logging.warning(f"⏰ Timeout ao executar CK em {repo_path}.")

def parse_ck_output(output_dir):
    class_csv = os.path.join(output_dir, "class.csv")
    if not os.path.exists(class_csv) or os.path.getsize(class_csv) == 0:
        return None, None, None
    df = pd.read_csv(class_csv)
    return (
        df["cbo"].mean() if "cbo" in df.columns else None,
        df["dit"].mean() if "dit" in df.columns else None,
        df["lcom"].mean() if "lcom" in df.columns else None
    )

def count_loc_comments(repo_path):
    loc = comentarios = 0
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.java'):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    in_block = False
                    for line in f:
                        line = line.strip()
                        if line:
                            loc += 1
                            if line.startswith("//") or in_block:
                                comentarios += 1
                            if "/*" in line:
                                comentarios += 1
                                in_block = True
                            if "*/" in line:
                                in_block = False
    return loc, comentarios

def calcular_maturidade(created_at_str):
    created_date = datetime.strptime(created_at_str[:10], "%Y-%m-%d")
    return round((datetime.today() - created_date).days / 365.25, 2)

def coletar_dados():
    logging.info("===== 📥 INICIANDO COLETA DE DADOS =====")
    inicio = time.time()

    df_repos = pd.read_csv(REPOS_LIST_FILE)
    total_repos = len(df_repos)
    resultados, contador = [], 0

    for idx, row in df_repos.iterrows():
        repo_url, created_at = row["clone_url"].strip(), row["created_at"].strip()
        stars = row["stars"] if "stars" in row else 0
        release = row["releases"] if "releases" in row else 0
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(REPOS_DIR, repo_name)

        idx_display = f"{idx+1:02}"
        log_prefix = f"({idx_display}/{total_repos})"
        padding = ' ' * len(log_prefix)

        logging.info(f"{log_prefix} 📂 Processando: \033[33m{repo_name}\033[0m")

        if not os.path.exists(repo_path):
            logging.warning(f"{padding} 📁 Diretório não encontrado: \033[35m{repo_name}\033[0m. Pulando...")
            continue

        ck_output_dir = os.path.join(DATA_DIR, f"ck_output_{repo_name}")
        class_csv = os.path.join(ck_output_dir, "class.csv")

        if os.path.exists(class_csv) and os.path.getsize(class_csv) > 0:
            logging.info(f"{padding} ✅ CK já coletado: \033[35m{repo_name}\033[0m")
            continue

        logging.info(f"{padding} 🔨 Executando análise CK...")
        run_ck(repo_path, ck_output_dir)

        logging.info(f"{padding} 📊 Extraindo métricas CK...")
        cbo, dit, lcom = parse_ck_output(ck_output_dir)

        logging.info(f"{padding} 📑 Contando LOC e comentários...")
        loc, comentarios = count_loc_comments(repo_path)

        logging.info(f"{padding} 📅 Calculando maturidade...")
        maturidade = calcular_maturidade(created_at)

        contador += 1
        logging.info(f"{padding} ✅ Dados coletados: \033[35m{repo_name}\033[0m (Total: {contador})")

        resultados.append({"repo_name": repo_name, "Stars": stars, "clone_url": repo_url, "Release": release, "CBO": cbo, "DIT": dit,
                           "LCOM": lcom, "LOC": loc, "Comments": comentarios, "Maturity": maturidade})

    pd.DataFrame(resultados).to_csv(os.path.join(DATA_DIR, "resultados_totais.csv"), index=False)

    fim = time.time()
    logging.info(f"🎯 Coleta finalizada! Total coletado: {contador} de {total_repos}")

    if contador < total_repos:
        logging.warning(f"⚠️ Apenas {contador} repositórios coletados. Esperado: {total_repos}")
        logging.error(f"❌ Foram coletados {contador} repositórios. Esperado: {total_repos}. Verifique! 📌")
    else:
        logging.info(f"✅ Todos os {total_repos} repositórios coletados com sucesso!")

if __name__ == "__main__":
    coletar_dados()