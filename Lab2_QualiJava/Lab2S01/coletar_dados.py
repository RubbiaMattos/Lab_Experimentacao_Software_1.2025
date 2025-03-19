import os
import csv
import subprocess
import pandas as pd
import logging
from datetime import datetime
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
CK_JAR = os.path.join(BASE_DIR, 'ck.jar')

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
CK_TIMEOUT = 300

def run_ck(repo_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    command = ['java', '-jar', CK_JAR, repo_path, "true", "0", "true", output_dir]
    logging.info(f"🔎 Executando CK para {repo_path}...")
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=CK_TIMEOUT)
        logging.info(f"✅ CK finalizado para {repo_path} -> {output_dir}")
    except subprocess.TimeoutExpired:
        logging.warning(f"⏰ Timeout CK em {repo_path} (>{CK_TIMEOUT}s). Pulando...")

def parse_ck_output(output_dir):
    class_csv = os.path.join(output_dir, "class.csv")
    try:
        if not os.path.exists(class_csv) or os.path.getsize(class_csv) == 0:
            logging.warning(f"⚠️ Arquivo {class_csv} vazio ou não existe.")
            return None, None, None
        df = pd.read_csv(class_csv)
        avg_cbo = df["CBO"].mean() if "CBO" in df.columns else None
        avg_dit = df["DIT"].mean() if "DIT" in df.columns else None
        avg_lcom = df["LCOM"].mean() if "LCOM" in df.columns else None
        return avg_cbo, avg_dit, avg_lcom
    except Exception as e:
        logging.error(f"❌ Erro ao ler {class_csv}: {e}")
        return None, None, None

def coletar_dados():
    if not os.path.exists(REPOS_LIST_FILE) or os.stat(REPOS_LIST_FILE).st_size == 0:
        raise ValueError(f"❌ {REPOS_LIST_FILE} não existe ou está vazio.")

    df_repos = pd.read_csv(REPOS_LIST_FILE)
    resultados = []

    for idx, row in df_repos.iterrows():
        repo_url = row["clone_url"].strip()
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(REPOS_DIR, repo_name)

        if not os.path.exists(repo_path):
            logging.warning(f"📂 Repositório {repo_name} não encontrado. Pulando...")
            continue

        ck_output_dir = os.path.join(DATA_DIR, f"ck_output_{repo_name}")

        if os.path.exists(os.path.join(ck_output_dir, "class.csv")):
            logging.info(f"✅ Métricas já coletadas para {repo_name}. Pulando...")
            continue

        run_ck(repo_path, ck_output_dir)
        avg_cbo, avg_dit, avg_lcom = parse_ck_output(ck_output_dir)

        resultados.append({
            "repo_name": repo_name,
            "clone_url": repo_url,
            "CBO": avg_cbo,
            "DIT": avg_dit,
            "LCOM": avg_lcom,
            "stars": row.get("stars"),
            "created_at": row.get("created_at"),
            "last_push": row.get("last_push")
        })

    output_csv = os.path.join(DATA_DIR, "resultados_totais.csv")
    pd.DataFrame(resultados).to_csv(output_csv, index=False)
    logging.info(f"💾 Resultados salvos em {output_csv}")

def main():
    logging.info("🚀 Iniciando coleta de dados e métricas CK...")
    try:
        coletar_dados()
    except Exception as e:
        logging.error(f"❌ Erro durante a coleta: {e}")

if __name__ == "__main__":
    main()
