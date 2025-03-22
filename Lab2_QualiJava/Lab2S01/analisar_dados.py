import os
import logging
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
from tabulate import tabulate


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

    colunas_necessarias = ['repo_name', 'clone_url', 'CBO', 'DIT', 'LCOM', 'LOC', 'Comments', 'Maturity', 'Release', 'Stars']
    if not all(col in df.columns for col in colunas_necessarias):
        logging.warning(f"⚠️ Faltam colunas obrigatórias: {colunas_necessarias}")
        return

    metricas = ['CBO', 'DIT', 'LCOM', 'LOC', 'Comments', 'Maturity', 'Release', 'Stars']
    logging.info("🧹 Limpando e preparando os dados...")

    for col in ['CBO', 'DIT', 'LCOM']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    for col in ['LOC', 'Comments', 'Maturity', 'Release', 'Stars']:
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

    logging.info("🔗 Gerando histogramas das variáveis...")
    plt.figure(figsize=(15, 10))

    # Para cada métrica, cria um histograma
    for i, metrica in enumerate(metricas, 1):
        # Exibindo os histogramas agrupados na tela
        plt.subplot(2, 4, i)
        plt.hist(df_metricas[metrica], bins=10, edgecolor='black', alpha=0.7)
        plt.title(f'Histograma de {metrica}')
        plt.xlabel(metrica)
        plt.ylabel('Frequência')

        # Salva o gráfico com o nome da métrica concatenado
        fig = plt.figure(figsize=(8, 6))
        plt.hist(df_metricas[metrica], bins=10, edgecolor='black', alpha=0.7)
        plt.title(f'Histograma de {metrica}')
        plt.xlabel(metrica)
        plt.ylabel('Frequência')
        plt.savefig(os.path.join(LOG_DIR, f'histograma_{metrica}.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)

    # Ajustar o layout para evitar sobreposição
    plt.tight_layout()
    plt.show()

    logging.info("✅ Histogramas gerados.\n")        

    try:
        stats.to_csv(output_file)
        logging.info(f"💾 Resultados estatísticos salvos no arquivo: {output_file}")      
    except Exception as e:
        logging.error(f"❌ Erro ao salvar resultados no arquivo '{output_file}': {e}")
        raise

    return df_metricas

def questao_pesquisa_01(df_metricas):
    print("\nRQ 01. Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?")

    # Lista de métricas
    metrics = ['CBO', 'DIT', 'LCOM']

    # Criando um dicionário para armazenar os resultados
    correlacao_results = []

    # Criando uma figura para exibir os gráficos agrupados
    plt.figure(figsize=(15, 12))

    # Criando gráficos de dispersão com linha de tendência para cada métrica
    for i, metric in enumerate(metrics, 1):
        # Exibindo os gráficos agrupados na tela
        plt.subplot(2, 2, i)
        sns.regplot(data=df_metricas, x='Stars', y=metric, scatter_kws={'s': 100, 'alpha': 0.7}, line_kws={'color': 'red', 'lw': 2})
        plt.title(f'Relação entre Popularidade (Stars) e {metric} com Linha de Tendência')
        plt.xlabel('Stars (Popularidade)')
        plt.ylabel(f'{metric}')
        
        # Salva cada gráfico individualmente
        fig = plt.figure(figsize=(8, 6))
        sns.regplot(data=df_metricas, x='Stars', y=metric, scatter_kws={'s': 100, 'alpha': 0.7}, line_kws={'color': 'red', 'lw': 2})
        plt.title(f'Relação entre Popularidade (Stars) e {metric} com Linha de Tendência')
        plt.xlabel('Stars (Popularidade)')
        plt.ylabel(f'{metric}')
        plt.savefig(os.path.join(LOG_DIR, f'popularidade_qualidade_{metric}.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)

    # Exibe todos os gráficos agrupados na tela
    plt.tight_layout()
    plt.show()

    print("\nGráficos salvos.")

    # Teste de correlação para cada métrica (Spearman e Pearson)
    for metric in metrics:
        # Cálculo da correlação de Pearson
        pearson_corr, pearson_p = pearsonr(df_metricas['Stars'], df_metricas[metric])
        # Cálculo da correlação de Spearman
        spearman_corr, spearman_p = spearmanr(df_metricas['Stars'], df_metricas[metric])
        
        # Armazenando os resultados no dicionário
        correlacao_results.append({
        'Metric': metric,
        'Pearson_Coefficient': pearson_corr,
        'Pearson_p-value': pearson_p,
        'Spearman_Coefficient': spearman_corr,
        'Spearman_p-value': spearman_p
        })

    # Convertendo o dicionário para um DataFrame do pandas
    correlacao_df = pd.DataFrame(correlacao_results)

    # Exibindo a tabela no terminal
    logging.info("\n" + tabulate(correlacao_df, headers='keys', tablefmt='grid'))

    # Salvando o DataFrame em um arquivo CSV
    correlacao_df.to_csv(os.path.join(LOG_DIR, 'correlacao_p_values_rq01.csv'), index=False)

    # Regressão linear mútilpla
    X = df_metricas[["CBO", "DIT", "LCOM", "LOC", "Comments", "Maturity", "Release"]]
    y = df_metricas["Stars"]

    # Adicionar constante para regressão
    X = sm.add_constant(X)

    # Ajustar modelo
    model = sm.OLS(y, X).fit()

    # Exibir resumo estatístico
    print(model.summary())

    logging.info("✅ Resultados de correlação salvos em 'correlacao_p_values_rq01.csv'.")


def questao_pesquisa_02(df_metricas):        
    print("\nRQ 02. Qual a relação entre a maturidade do repositórios e as suas características de qualidade ?")

    # Lista de métricas
    metrics = ['CBO', 'DIT', 'LCOM']

    # Criando um dicionário para armazenar os resultados
    correlacao_results = []

    # Criando uma figura para exibir os gráficos agrupados
    plt.figure(figsize=(15, 12))

    # Criando gráficos de dispersão com linha de tendência para cada métrica
    for i, metric in enumerate(metrics, 1):
        # Exibindo os gráficos agrupados na tela
        plt.subplot(2, 2, i)
        sns.regplot(data=df_metricas, x='Maturity', y=metric, scatter_kws={'s': 100, 'alpha': 0.7}, line_kws={'color': 'red', 'lw': 2})
        plt.title(f'Relação entre Maturidade e {metric} com Linha de Tendência')
        plt.xlabel('Maturidade')
        plt.ylabel(f'{metric}')
        
        # Salva cada gráfico individualmente
        fig = plt.figure(figsize=(8, 6))
        sns.regplot(data=df_metricas, x='Maturity', y=metric, scatter_kws={'s': 100, 'alpha': 0.7}, line_kws={'color': 'red', 'lw': 2})
        plt.title(f'Relação entre Maturidade e {metric} com Linha de Tendência')
        plt.xlabel('Maturidade')
        plt.ylabel(f'{metric}')
        plt.savefig(os.path.join(LOG_DIR, f'maturidade_qualidade_{metric}.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)

    # Ajustar o layout para evitar sobreposição
    plt.tight_layout()
    plt.show()

    print("\nGráficos salvos.")

    # Teste de correlação para cada métrica (Spearman e Pearson)
    for metric in metrics:
        # Cálculo da correlação de Pearson
        pearson_corr, pearson_p = pearsonr(df_metricas['Maturity'], df_metricas[metric])
        # Cálculo da correlação de Spearman
        spearman_corr, spearman_p = spearmanr(df_metricas['Maturity'], df_metricas[metric])
        
        # Armazenando os resultados no dicionário
        correlacao_results.append({
        'Metric': metric,
        'Pearson_Coefficient': pearson_corr,
        'Pearson_p-value': pearson_p,
        'Spearman_Coefficient': spearman_corr,
        'Spearman_p-value': spearman_p
        })

    # Convertendo o dicionário para um DataFrame do pandas
    correlacao_df = pd.DataFrame(correlacao_results)

    # Exibindo a tabela no terminal
    logging.info("\n" + tabulate(correlacao_df, headers='keys', tablefmt='grid'))

    # Salvando o DataFrame em um arquivo CSV
    correlacao_df.to_csv(os.path.join(LOG_DIR, 'correlacao_p_values_rq02.csv'), index=False)

    # Regressão linear mútilpla
    X = df_metricas[["CBO", "DIT", "LCOM", "LOC", "Comments", "Release", "Stars"]]
    y = df_metricas["Maturity"]

    # Adicionar constante para regressão
    X = sm.add_constant(X)

    # Ajustar modelo
    model = sm.OLS(y, X).fit()

    # Exibir resumo estatístico
    print(model.summary())

    logging.info("✅ Resultados de correlação salvos em 'correlacao_p_values_rq02.csv'.")


def questao_pesquisa_03(df_metricas):        
    print("\nRQ 03. Qual a relação entre a atividade dos repositórios e as suas características de qualidade?")

    # Lista de métricas
    metrics = ['CBO', 'DIT', 'LCOM']

    # Criando um dicionário para armazenar os resultados
    correlacao_results = []

   # Criando uma figura para exibir os gráficos agrupados
    plt.figure(figsize=(15, 12))

    # Criando gráficos de dispersão com linha de tendência para cada métrica
    for i, metric in enumerate(metrics, 1):
        # Exibindo os gráficos agrupados na tela
        plt.subplot(2, 2, i)
        sns.regplot(data=df_metricas, x='Release', y=metric, scatter_kws={'s': 100, 'alpha': 0.7}, line_kws={'color': 'red', 'lw': 2})
        plt.title(f'Relação entre Release e {metric} com Linha de Tendência')
        plt.xlabel('Release')
        plt.ylabel(f'{metric}')
        
        # Salva cada gráfico individualmente
        fig = plt.figure(figsize=(8, 6))
        sns.regplot(data=df_metricas, x='Release', y=metric, scatter_kws={'s': 100, 'alpha': 0.7}, line_kws={'color': 'red', 'lw': 2})
        plt.title(f'Relação entre Release e {metric} com Linha de Tendência')
        plt.xlabel('Release')
        plt.ylabel(f'{metric}')
        plt.savefig(os.path.join(LOG_DIR, f'release_qualidade_{metric}.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)

    # Ajustar o layout para evitar sobreposição
    plt.tight_layout()
    plt.show()

    print("\nGráficos salvos.")
    
    # Teste de correlação para cada métrica (Spearman e Pearson)
    for metric in metrics:
        # Cálculo da correlação de Pearson
        pearson_corr, pearson_p = pearsonr(df_metricas['Release'], df_metricas[metric])
        # Cálculo da correlação de Spearman
        spearman_corr, spearman_p = spearmanr(df_metricas['Release'], df_metricas[metric])
        
        # Armazenando os resultados no dicionário
        correlacao_results.append({
        'Metric': metric,
        'Pearson_Coefficient': pearson_corr,
        'Pearson_p-value': pearson_p,
        'Spearman_Coefficient': spearman_corr,
        'Spearman_p-value': spearman_p
        })

    # Convertendo o dicionário para um DataFrame do pandas
    correlacao_df = pd.DataFrame(correlacao_results)

    # Exibindo a tabela no terminal
    logging.info("\n" + tabulate(correlacao_df, headers='keys', tablefmt='grid'))

    # Salvando o DataFrame em um arquivo CSV
    correlacao_df.to_csv(os.path.join(LOG_DIR, 'correlacao_p_values_rq03.csv'), index=False)

    # Regressão linear mútilpla
    X = df_metricas[["CBO", "DIT", "LCOM", "LOC", "Comments", "Maturity", "Stars"]]
    y = df_metricas["Release"]

    # Adicionar constante para regressão
    X = sm.add_constant(X)

    # Ajustar modelo
    model = sm.OLS(y, X).fit()

    # Exibir resumo estatístico
    print(model.summary())

    logging.info("✅ Resultados de correlação salvos em 'correlacao_p_values_rq03.csv'.")


def questao_pesquisa_04(df_metricas):        
    print("\nRQ 04. Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?")

    # Lista de métricas
    metrics = ['CBO', 'DIT', 'LCOM']

    # Criando um dicionário para armazenar os resultados
    correlacao_results = []

    # Criando uma figura para exibir os gráficos agrupados
    plt.figure(figsize=(15, 12))

    # Criando gráficos de dispersão com linha de tendência para cada métrica
    for i, metric in enumerate(metrics, 1):
        # Exibindo os gráficos agrupados na tela
        plt.subplot(2, 2, i)
        sns.regplot(data=df_metricas, x='LOC', y=metric, scatter_kws={'s': 100, 'alpha': 0.7}, line_kws={'color': 'red', 'lw': 2})
        plt.title(f'Relação entre Tamanho (LOC) e {metric} com Linha de Tendência')
        plt.xlabel('LOC')
        plt.ylabel(f'{metric}')
        
        # Salva cada gráfico individualmente
        fig = plt.figure(figsize=(8, 6))
        sns.regplot(data=df_metricas, x='LOC', y=metric, scatter_kws={'s': 100, 'alpha': 0.7}, line_kws={'color': 'red', 'lw': 2})
        plt.title(f'Relação entre Tamanho (LOC) e {metric} com Linha de Tendência')
        plt.xlabel('LOC')
        plt.ylabel(f'{metric}')
        plt.savefig(os.path.join(LOG_DIR, f'loc_qualidade_{metric}.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)

    # Ajustar o layout para evitar sobreposição
    plt.tight_layout()
    plt.show()

    print("\nGráficos salvos.")

    # Teste de correlação para cada métrica (Spearman e Pearson)
    for metric in metrics:
        # Cálculo da correlação de Pearson
        pearson_corr, pearson_p = pearsonr(df_metricas['LOC'], df_metricas[metric])
        # Cálculo da correlação de Spearman
        spearman_corr, spearman_p = spearmanr(df_metricas['LOC'], df_metricas[metric])
        
        # Armazenando os resultados no dicionário
        correlacao_results.append({
        'Metric': metric,
        'Pearson_Coefficient': pearson_corr,
        'Pearson_p-value': pearson_p,
        'Spearman_Coefficient': spearman_corr,
        'Spearman_p-value': spearman_p
        })

    # Convertendo o dicionário para um DataFrame do pandas
    correlacao_df = pd.DataFrame(correlacao_results)

    # Exibindo a tabela no terminal
    logging.info("\n" + tabulate(correlacao_df, headers='keys', tablefmt='grid'))

    # Salvando o DataFrame em um arquivo CSV
    correlacao_df.to_csv(os.path.join(LOG_DIR, 'correlacao_p_values_rq04.csv'), index=False)    

    # Regressão linear mútilpla
    X = df_metricas[["CBO", "DIT", "LCOM", "Comments", "Maturity", "Release", "Stars"]]
    y = df_metricas["LOC"]

    # Adicionar constante para regressão
    X = sm.add_constant(X)

    # Ajustar modelo
    model = sm.OLS(y, X).fit()

    # Exibir resumo estatístico
    print(model.summary())

    logging.info("✅ Resultados de correlação salvos em 'correlacao_p_values_rq04.csv'.")


def main():
    logging.info("===== 🚀 INICIANDO PROCESSO DE ANÁLISE =====")
    try:
        input_file = verificar_arquivo_entrada()
        if input_file:
            print("\n🔹 Analisando os dados e gerando resultados gerais...")
            df = analisar_dados(input_file)

            print("\nGerando resultados da RQ 01...")
            questao_pesquisa_01(df)

            print("\nGerando resultados da RQ 02...")
            questao_pesquisa_02(df)

            print("\nGerando resultados da RQ 03...")
            questao_pesquisa_03(df)

            print("\nGerando resultados da RQ 04...")
            questao_pesquisa_04(df)
        else:
            logging.info("ℹ️ Nenhum dado para analisar. Processo encerrado.")
        logging.info("🎉 Processo de análise finalizado com sucesso!")
    except Exception as e:
        logging.error(f"❌ Processo encerrado com erro: {e}")
        raise

if __name__ == "__main__":
    main()