import os
import logging
import pandas as pd

# Configuração dos diretórios base e da pasta de dados
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, 'data'))

# Configuração do logger
script_dir = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(script_dir, "Relatórios")
LOG_FILE = os.path.join(LOG_DIR, "analisar_dados_log.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE, encoding="utf-8")]
)

def verificar_arquivo_entrada():
    input_file = os.path.join(DATA_DIR, 'resultados_totais.csv')
    logging.info("🔍 Verificando existência e integridade do arquivo de entrada...")

    if not os.path.exists(input_file):
        logging.error(f"❌ Arquivo não encontrado: {input_file}")
        raise FileNotFoundError(f"❌ Arquivo não encontrado: {input_file}")

    if os.stat(input_file).st_size == 0:
        logging.warning(f"⚠️ Arquivo vazio encontrado: {input_file}")
        return None

    logging.info(f"✅ Arquivo de entrada verificado com sucesso: {input_file}")
    return input_file

def analisar_dados(input_file):
    logging.info("📊 Iniciando análise dos dados coletados...")
    output_file = os.path.join(DATA_DIR, 'analise_metrica_ck.csv')

    try:
        df = pd.read_csv(input_file)
        logging.info(f"📥 Arquivo '{input_file}' carregado. {len(df)} registros encontrados.")
    except pd.errors.EmptyDataError:
        logging.warning(f"⚠️ Arquivo de entrada está vazio ou corrompido: {input_file}")
        return
    except Exception as e:
        logging.error(f"❌ Erro inesperado ao ler o arquivo '{input_file}': {e}")
        raise

    colunas_necessarias = ['repo_name', 'clone_url', 'CBO', 'DIT', 'LCOM', 'LOC', 'Comments', 'Maturity']
    if not all(col in df.columns for col in colunas_necessarias):
        logging.warning(f"⚠️ Faltam colunas obrigatórias: {colunas_necessarias}")
        return

    metricas = ['CBO', 'DIT', 'LCOM', 'LOC', 'Comments', 'Maturity']
    logging.info("🧹 Limpando e preparando os dados...")

    for col in ['CBO', 'DIT', 'LCOM']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    for col in ['LOC', 'Comments', 'Maturity']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df_metricas = df[metricas].dropna()
    registros_validos = len(df_metricas)
    logging.info(f"📈 Registros válidos após limpeza: {registros_validos} de {len(df)} totais.")

    if df_metricas.empty:
        logging.warning("⚠️ Nenhum dado válido disponível após limpeza. Análise cancelada.")
        return

    logging.info("📉 Calculando estatísticas descritivas...")
    stats = df_metricas.describe()
    logging.info("✅ Estatísticas calculadas com sucesso:\n" + stats.to_string())

    logging.info("🔗 Calculando matriz de correlação...")
    correlacoes = df_metricas.corr()
    logging.info("✅ Matriz de correlação calculada:\n" + correlacoes.to_string())

    try:
        stats.to_csv(output_file)
        logging.info(f"💾 Resultados estatísticos salvos no arquivo: {output_file}")
    except Exception as e:
        logging.error(f"❌ Erro ao salvar resultados no arquivo '{output_file}': {e}")
        raise

def main():
    logging.info("===== 🚀 INICIANDO PROCESSO DE ANÁLISE =====")
    try:
        input_file = verificar_arquivo_entrada()
        if input_file:
            analisar_dados(input_file)
        else:
            logging.info("ℹ️ Nenhum dado para analisar. Processo encerrado.")
        logging.info("🎉 Processo de análise finalizado com sucesso!")
    except Exception as e:
        logging.error(f"❌ Processo encerrado com erro: {e}")
        raise

if __name__ == "__main__":
    main()