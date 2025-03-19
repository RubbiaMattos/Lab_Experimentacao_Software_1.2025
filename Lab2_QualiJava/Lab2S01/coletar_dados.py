import os
import csv
import subprocess
import pandas as pd
import logging
from datetime import datetime
import argparse
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.abspath(os.path.join(script_dir, "..", "..", ".env.config"))

if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    raise FileNotFoundError(f"❌ ERRO: O arquivo .env.config NÃO foi encontrado: {env_path}")

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise ValueError("❌ ERRO: Token GITHUB_TOKEN não foi encontrado no .env.config 🔑")

# Configuração de diretórios
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPOS_DIR = os.path.join(DATA_DIR, 'repos')
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')
CK_JAR = os.path.join(BASE_DIR, 'ck.jar')  # ck.jar deve estar na raiz do projeto

# Configuração do logger
# 🔹 Caminho relativo para salvar os logs
LOG_DIR = os.path.join(script_dir, "Relatórios")
LOG_FILE = os.path.join(LOG_DIR, "coletar_dados_log.log")

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

# Timeout para execução do CK (em segundos)
CK_TIMEOUT = 300

def run_ck(repo_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    if not output_dir.endswith(os.sep):
        output_dir += os.sep

    command = [
        'java', '-jar', CK_JAR,
        repo_path, "true", "0", "true", output_dir
    ]
    logging.debug(f"🚀 Executando comando CK: {' '.join(command)}")
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=CK_TIMEOUT)
        if result.returncode != 0:
            logging.warning(f"⚠️ Erro ao executar CK em {repo_path}: retorno {result.returncode}\nStderr: {result.stderr.decode(errors='ignore')}")
        else:
            logging.info(f"✅ CK executado para {repo_path}. Saída no diretório {output_dir}")
    except subprocess.TimeoutExpired:
        logging.warning(f"⏰ Timeout ao executar CK em {repo_path} (>{CK_TIMEOUT} segundos). Pulando repositório.")
    except Exception as e:
        logging.error(f"❌ Exceção ao executar CK em {repo_path}: {e}")

def parse_ck_output(output_dir):
    class_csv = os.path.join(output_dir, "class.csv")
    try:
        if not os.path.exists(class_csv) or os.path.getsize(class_csv) == 0:
            logging.warning(f"⚠️ Arquivo {class_csv} está vazio ou não existe.")
            return None, None, None

        df = pd.read_csv(class_csv)
        logging.debug(f"📄 Dados lidos de {class_csv} (primeiras 5 linhas):\n{df.head()}")
        if df.empty:
            logging.warning(f"⚠️ O arquivo {class_csv} não contém dados.")
            return None, None, None

        avg_cbo = df["cbo"].mean() if "cbo" in df.columns else None
        avg_dit = df["dit"].mean() if "dit" in df.columns else None
        avg_lcom = df["lcom"].mean() if "lcom" in df.columns else None
        logging.debug(f"📊 Métricas extraídas -> CBO: {avg_cbo}, DIT: {avg_dit}, LCOM: {avg_lcom}")
        return avg_cbo, avg_dit, avg_lcom
    except Exception as e:
        logging.error(f"❌ Erro ao ler CK output {class_csv}: {e}")
        return None, None, None

def count_loc_comments(repo_path):
    total_loc = 0
    total_comments = 0
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        in_block = False
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            total_loc += 1
                            if line.startswith("//"):
                                total_comments += 1
                            elif "/*" in line:
                                total_comments += 1
                                in_block = True
                            elif in_block:
                                total_comments += 1
                                if "*/" in line:
                                    in_block = False
                except Exception as e:
                    logging.error(f"❌ Erro ao ler {file_path}: {e}")
    logging.debug(f"📈 Para {repo_path} -> LOC: {total_loc}, Comentários: {total_comments}")
    return total_loc, total_comments

def calcular_maturidade(created_at_str):
    try:
        created_date = datetime.strptime(created_at_str[:10], "%Y-%m-%d")
        today = datetime.today()
        maturity = (today - created_date).days / 365.25
        return round(maturity, 2)
    except Exception as e:
        logging.error(f"❌ Erro ao calcular maturidade para {created_at_str}: {e}")
        return None

def coletar_dados():
    if not os.path.exists(REPOS_LIST_FILE) or os.stat(REPOS_LIST_FILE).st_size == 0:
        raise ValueError(f"❌ Arquivo {REPOS_LIST_FILE} não existe ou está vazio.")

    logging.info(f"📥 Lendo arquivo de repositórios: {REPOS_LIST_FILE}")
    df_repos = pd.read_csv(REPOS_LIST_FILE, header=None, names=["clone_url"])
    logging.debug(f"🔎 Primeiras 5 linhas do CSV de repositórios:\n{df_repos.head()}")
    resultados = []
    total_repos = len(df_repos)
    contador = 0

    for idx, row in df_repos.iterrows():
        repo_url = row["clone_url"].strip()
        if not repo_url:
            logging.debug("⚠️ Linha vazia encontrada; pulando...")
            continue

        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(REPOS_DIR, repo_name)

        if not os.path.exists(repo_path):
            logging.warning(f"📂 Diretório do repositório {repo_name} não encontrado. Pulando...")
            continue

        ck_output_dir = os.path.join(DATA_DIR, f"ck_output_{repo_name}")
        class_csv = os.path.join(ck_output_dir, "class.csv")
        if os.path.exists(class_csv) and os.path.getsize(class_csv) > 0:
            logging.info(f"✅ Dados do repositório {repo_name} já foram coletados. Pulando...")
            contador += 1
            continue

        logging.info(f"🔨 Iniciando processamento do repositório: {repo_name}")
        run_ck(repo_path, ck_output_dir)

        avg_cbo, avg_dit, avg_lcom = parse_ck_output(ck_output_dir)
        loc, comentarios = count_loc_comments(repo_path)
        created_at = "2000-01-01"  # Valor dummy; ajuste se possuir dados reais.
        maturity = calcular_maturidade(created_at)

        contador += 1
        logging.info(f"📦 ({contador}/{total_repos}) Dados coletados para {repo_name} ✅")

        repo_data = {
            "repo_name": repo_name,
            "clone_url": repo_url,
            "CBO": avg_cbo,
            "DIT": avg_dit,
            "LCOM": avg_lcom,
            "LOC": loc,
            "Comments": comentarios,
            "Maturity": maturity
        }
        resultados.append(repo_data)

    output_csv = os.path.join(DATA_DIR, "resultados_totais.csv")
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(output_csv, index=False)
    logging.info(f"📊 Resultados consolidados salvos em {output_csv} ✅")

def main():
    logging.info("🚀 Iniciando coleta de dados e métricas CK dos repositórios clonados...")
    try:
        coletar_dados()
    except Exception as e:
        logging.error(f"❌ Erro durante a coleta das métricas: {e}")

if __name__ == "__main__":
    main()
