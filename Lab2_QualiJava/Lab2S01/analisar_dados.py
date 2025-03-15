import os
import logging
import pandas as pd

# Configuração de diretórios base e pasta de dados
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, 'data'))

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def verificar_arquivo_entrada():
    """
    Verifica se o arquivo de entrada 'resultados_totais.csv' existe e não está vazio.
    Esse arquivo deve ter sido gerado pelo script coletar_dados.py.
    """
    input_file = os.path.join(DATA_DIR, 'resultados_totais.csv')
    if not os.path.exists(input_file):
        logging.error(f"Arquivo de entrada não encontrado: {input_file}")
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_file}")
    if os.stat(input_file).st_size == 0:
        logging.warning(f"Arquivo de entrada está vazio: {input_file}")
        return None
    logging.info(f"Arquivo de entrada validado: {input_file}")
    return input_file

def analisar_dados(input_file):
    """
    Realiza a análise dos dados do arquivo 'resultados_totais.csv' gerado pelo coletar_dados.py:
      - Converte as colunas de métricas para valores numéricos.
      - Preenche as colunas de CK (CBO, DIT, LCOM) com 0 caso estejam vazias.
      - Remove registros com NaN nas colunas essenciais (LOC, Comments, Maturity).
      - Calcula estatísticas descritivas e a matriz de correlação.
      - Salva os resultados em 'analise_metrica_ck.csv'.
    """
    output_file = os.path.join(DATA_DIR, 'analise_metrica_ck.csv')
    logging.info("Iniciando a análise de dados...")

    try:
        df = pd.read_csv(input_file)
        logging.info(f"Arquivo de entrada '{input_file}' carregado com sucesso.")
    except pd.errors.EmptyDataError:
        logging.warning(f"Arquivo de entrada está vazio ou corrompido: {input_file}")
        return
    except Exception as e:
        logging.error(f"Erro ao carregar o arquivo '{input_file}': {e}")
        raise

    # Colunas que esperamos (conforme gerado pelo coletar_dados.py)
    colunas_necessarias = ['repo_name', 'clone_url', 'CBO', 'DIT', 'LCOM', 'LOC', 'Comments', 'Maturity']
    if not all(col in df.columns for col in colunas_necessarias):
        logging.warning(f"As colunas necessárias {colunas_necessarias} não foram encontradas no arquivo de entrada.")
        return

    metricas = ['CBO', 'DIT', 'LCOM', 'LOC', 'Comments', 'Maturity']

    # Converter as colunas de métricas para numérico
    for col in ['CBO', 'DIT', 'LCOM']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    for col in ['LOC', 'Comments', 'Maturity']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remover linhas onde LOC, Comments ou Maturity são NaN
    df_metricas = df[metricas].dropna()
    logging.info(f"Após conversão e remoção de NaN, {len(df_metricas)} registros serão analisados de um total de {len(df)}.")

    if df_metricas.empty:
        logging.warning("Nenhum dado numérico válido encontrado após a conversão. Verifique o arquivo de entrada.")
        return

    # Estatísticas descritivas
    stats = df_metricas.describe()
    logging.info("Estatísticas descritivas das métricas do CK (NaN removidos):")
    logging.info("\n" + stats.to_string())

    # Matriz de correlação
    correlacoes = df_metricas.corr()
    logging.info("Matriz de correlação entre as métricas do CK (NaN removidos):")
    logging.info("\n" + correlacoes.to_string())

    # Salvar os resultados da análise em um arquivo CSV
    try:
        stats.to_csv(output_file)
        logging.info(f"Resultados da análise salvos no arquivo: {output_file}")
    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo de saída '{output_file}': {e}")
        raise

def main():
    logging.info("Executando o script de análise de dados com métricas do CK (valores NaN tratados)...")
    try:
        input_file = verificar_arquivo_entrada()
        if input_file:
            analisar_dados(input_file)
        else:
            logging.info("Nenhuma análise foi realizada, pois o arquivo de entrada está vazio.")
        logging.info("Script de análise concluído.")
    except Exception as e:
        logging.error(f"Erro durante a execução do script de análise de dados: {e}")
        raise

if __name__ == "__main__":
    main()
