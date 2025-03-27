import os
import subprocess
import pandas as pd
import logging
import time
import shutil
from datetime import datetime
from config_token import configurar_token

TOKEN = configurar_token()

script_dir = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'Data')
REPOS_DIR = os.path.abspath(os.path.join(BASE_DIR, 'Repos'))
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')
CK_JAR = os.path.join(BASE_DIR, 'ck.jar')

LOG_DIR = os.path.join(script_dir, "Relatórios")
LOG_FILE = os.path.join(LOG_DIR, "coletar_dados.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)

CK_TIMEOUT = 300

def run_ck(repo_path, output_dir, idx_display, total_repos):
    tentativa = 0
    while tentativa < 2:
        temp_ck_dir = os.path.join(DATA_DIR, "temp_ck")
        os.makedirs(temp_ck_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        command = ['java', '-jar', CK_JAR, repo_path, "true", "0", "true"]

        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=CK_TIMEOUT, cwd=temp_ck_dir)
        except subprocess.TimeoutExpired:
            logging.warning(f"⏰ Timeout ao executar CK em {repo_path}.")
            shutil.rmtree(temp_ck_dir, ignore_errors=True)
            tentativa += 1
            continue

        expected_files = ["class.csv", "method.csv", "field.csv", "variable.csv"]
        missing_files = []

        log_prefix = f"({idx_display}/{total_repos})"
        padding = ' ' * len(log_prefix)

        logging.info(f"{padding} 📊 Coletando métricas CK (CBO, DIT, LCOM)...")

        for file_name in expected_files:
            src = os.path.join(temp_ck_dir, file_name)  # <-- ALTERADO
            dst = os.path.join(output_dir, file_name)


            if os.path.exists(src) and os.path.getsize(src) > 0:
                shutil.move(src, dst)
                if file_name == "class.csv":
                    logging.info(f"{padding}   📄 \033[92mclass.csv\033[0m - Métricas por classe.")
                elif file_name == "field.csv":
                    logging.info(f"{padding}   📄 \033[92mfield.csv\033[0m - Atributos da classe.")
                elif file_name == "method.csv":
                    logging.info(f"{padding}   📄 \033[92mmethod.csv\033[0m - Detalhes dos métodos.")
                elif file_name == "variable.csv":
                    logging.info(f"{padding}   📄 \033[92mvariable.csv\033[0m - Variáveis locais.")
            else:
                logging.error(f"{padding} ❌ Arquivo faltando ou vazio: {file_name} | Repositório: {repo_path}")
                missing_files.append(file_name)

        shutil.rmtree(temp_ck_dir, ignore_errors=True)

        if missing_files:
            if tentativa == 0:
                logging.warning(f"{padding} ⚠️ CK gerou arquivos faltando. Tentando rodar novamente...")
                tentativa += 1
                continue
            else:
                return False

        relative_output_dir = os.path.relpath(output_dir, BASE_DIR)
        logging.info(f"{padding} ✅ CK executado com sucesso. Arquivos salvos na pasta {relative_output_dir}")
        return True
    
    return False


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
        stars = row.get("stars", 0)
        release = row.get("releases", 0)
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(REPOS_DIR, repo_name)

        idx_display = f"{idx+1:02}"
        log_prefix = f"({idx_display}/{total_repos})"
        padding = ' ' * len(log_prefix)

        logging.info(f"{log_prefix} \033[4m\033[96m📂 Processando: \033[1m{repo_name}\033[0m")

        if not os.path.exists(repo_path):
            logging.warning(f"{padding} 📁 Diretório não encontrado: \033[92m{repo_name}\033[0m. Pulando...")
            continue

        ck_output_dir = os.path.join(DATA_DIR, f"ck_output_{repo_name}")
        os.makedirs(ck_output_dir, exist_ok=True)


        if os.path.exists(ck_output_dir):
            logging.info(f"{padding} ♻️ Removendo saída anterior do CK para \033[92m{repo_name}\033[0m")
            shutil.rmtree(ck_output_dir)

        os.makedirs(ck_output_dir, exist_ok=True)

        logging.info(f"{padding} 🔨 Executando análise CK...")
        success = run_ck(repo_path, ck_output_dir, idx_display, total_repos)

        if not success:
            logging.error(f"{padding} ❌ CK falhou ou arquivos faltando para \033[92m{repo_name}\033[0m. Pulando...")
            continue

        cbo, dit, lcom = parse_ck_output(ck_output_dir)

        logging.info(f"{padding} 📑 Contando Linhas de Código (LOC) e Comentários...")
        loc, comentarios = count_loc_comments(repo_path)

        logging.info(f"{padding} 📅 Calculando Maturidade do Projeto...")
        maturidade = calcular_maturidade(created_at)

        contador += 1
        logging.info(f"{padding} ✅ Dados coletados: \033[92m{repo_name}\033[0m (Total: {contador})")

        resultados.append({
            "repo_name": repo_name,
            "Stars": stars,
            "clone_url": repo_url,
            "Release": release,
            "CBO": cbo,
            "DIT": dit,
            "LCOM": lcom,
            "LOC": loc,
            "Comments": comentarios,
            "Maturity": maturidade
        })

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