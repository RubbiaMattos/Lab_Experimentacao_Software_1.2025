import os
import csv
import subprocess
import pandas as pd
import logging
from datetime import datetime
import argparse
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()

# Configuração de diretórios
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPOS_DIR = os.path.join(DATA_DIR, 'repos')
REPOS_LIST_FILE = os.path.join(DATA_DIR, 'repositorios_list.csv')
CK_JAR = os.path.join(BASE_DIR, 'ck.jar')  # ck.jar deve estar na raiz do projeto

# Configuração do logger
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def run_ck(repo_path, output_path):
    """
    Executa a ferramenta CK para o repositório indicado.
    O output (CSV) é salvo em output_path.
    Se a execução falhar, registra um warning e continua.
    """
    command = ['java', '-jar', CK_JAR, repo_path]
    logging.debug(f"Executando comando CK: {' '.join(command)}")
    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            result = subprocess.run(command, stdout=outfile, stderr=subprocess.PIPE)
        if result.returncode != 0:
            logging.warning(f"Erro ao executar CK em {repo_path}: código de retorno {result.returncode}")
        else:
            logging.info(f"CK executado para {repo_path}. Saída em {output_path}")
    except Exception as e:
        logging.error(f"Exceção ao executar CK em {repo_path}: {e}")

def parse_ck_output(output_path):
    """
    Lê o arquivo CSV gerado pelo CK e retorna as médias das métricas CBO, DIT e LCOM.
    Se o arquivo estiver vazio ou não contiver dados, retorna (None, None, None).
    """
    try:
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            logging.warning(f"Arquivo {output_path} está vazio ou não existe.")
            return None, None, None

        df = pd.read_csv(output_path)
        logging.debug(f"Dados lidos de {output_path} (primeiras 5 linhas):\n{df.head()}")
        if df.empty:
            logging.warning(f"O arquivo {output_path} não contém dados.")
            return None, None, None

        avg_cbo = df["CBO"].mean() if "CBO" in df.columns else None
        avg_dit = df["DIT"].mean() if "DIT" in df.columns else None
        avg_lcom = df["LCOM"].mean() if "LCOM" in df.columns else None
        logging.debug(f"Métricas extraídas de {output_path} -> CBO: {avg_cbo}, DIT: {avg_dit}, LCOM: {avg_lcom}")
        return avg_cbo, avg_dit, avg_lcom
    except Exception as e:
        logging.error(f"Erro ao ler CK output {output_path}: {e}")
        return None, None, None

def count_loc_comments(repo_path):
    """
    Percorre os arquivos .java do repositório para contar:
      - LOC: número de linhas não vazias
      - Comentários: linhas que começam com '//' ou que estão em blocos de comentário.
    """
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
                    logging.error(f"Erro ao ler {file_path}: {e}")
    logging.debug(f"Para {repo_path} -> LOC: {total_loc}, Comments: {total_comments}")
    return total_loc, total_comments

def calcular_maturidade(created_at_str):
    """
    Calcula a maturidade do repositório (em anos) com base na data de criação.
    O formato esperado é 'YYYY-MM-DD'. (Aqui usamos um valor dummy se não disponível.)
    """
    try:
        created_date = datetime.strptime(created_at_str[:10], "%Y-%m-%d")
        today = datetime.today()
        maturity = (today - created_date).days / 365.25
        return round(maturity, 2)
    except Exception as e:
        logging.error(f"Erro ao calcular maturidade para {created_at_str}: {e}")
        return None

def coletar_dados():
    """
    Processa cada repositório listado em repositorios_list.csv:
      - Executa o CK para extrair métricas (CBO, DIT, LCOM).
      - Conta LOC e linhas de comentários.
      - Calcula a maturidade (valor dummy neste exemplo).
      - Consolida os dados em resultados_totais.csv.
    """
    if not os.path.exists(REPOS_LIST_FILE) or os.stat(REPOS_LIST_FILE).st_size == 0:
        raise ValueError(f"Arquivo {REPOS_LIST_FILE} não existe ou está vazio.")

    logging.info(f"Lendo arquivo de repositórios: {REPOS_LIST_FILE}")
    df_repos = pd.read_csv(REPOS_LIST_FILE, header=None, names=["clone_url"])
    logging.debug(f"Primeiras 5 linhas do CSV de repositórios:\n{df_repos.head()}")
    resultados = []
    total_repos = len(df_repos)
    contador = 0

    for idx, row in df_repos.iterrows():
        repo_url = row["clone_url"].strip()
        if not repo_url:
            logging.debug("Linha vazia encontrada; pulando...")
            continue

        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(REPOS_DIR, repo_name)

        if not os.path.exists(repo_path):
            logging.warning(f"Diretório do repositório {repo_name} não encontrado. Pulando...")
            continue

        logging.info(f"Iniciando processamento do repositório: {repo_name}")
        ck_output_file = os.path.join(DATA_DIR, f"ck_output_{repo_name}.csv")
        run_ck(repo_path, ck_output_file)

        avg_cbo, avg_dit, avg_lcom = parse_ck_output(ck_output_file)
        loc, comentarios = count_loc_comments(repo_path)
        created_at = "2000-01-01"  # Valor dummy; ajuste se tiver dados reais.
        maturity = calcular_maturidade(created_at)

        contador += 1
        logging.info(f"({contador}/{total_repos}) Dados coletados para {repo_name}")

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
    logging.info(f"Resultados consolidados salvos em {output_csv}")

def main():
    logging.info("Iniciando coleta de dados e métricas CK dos repositórios clonados...")
    try:
        coletar_dados()
    except Exception as e:
        logging.error(f"Erro durante a coleta das métricas: {e}")

if __name__ == "__main__":
    main()
