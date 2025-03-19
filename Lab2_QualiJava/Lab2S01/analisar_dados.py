# analisar_dados.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os
import shutil

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def verificar_arquivo_entrada():
    pasta_dados = os.path.join('data', 'coletados')
    arquivos = [f for f in os.listdir(pasta_dados) if f.endswith('.csv')]
    if arquivos:
        logging.info(f"📄 Arquivo de entrada encontrado: {arquivos[0]}")
        return os.path.join(pasta_dados, arquivos[0])
    else:
        logging.warning("⚠️ Nenhum arquivo de entrada encontrado na pasta data/coletados.")
        return None

def analisar_dados(arquivo):
    logging.info("🔎 Carregando dados...")
    df = pd.read_csv(arquivo)

    logging.info("🛠 Tratando valores NaN...")
    df.fillna(0, inplace=True)

    logging.info("📊 Calculando estatísticas básicas...")
    estatisticas = df.describe()
    estatisticas.to_csv(os.path.join('data', 'relatorio_estatisticas.csv'))
    logging.info("✅ Estatísticas básicas salvas em data/relatorio_estatisticas.csv")

    logging.info("📈 Calculando a correlação entre as métricas...")
    correlacao = df.corr()
    correlacao.to_csv(os.path.join('data', 'relatorio_correlacao.csv'))
    logging.info("✅ Matriz de correlação salva em data/relatorio_correlacao.csv")

    logging.info("📉 Gerando o mapa de calor das correlações...")
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlacao, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Mapa de Calor da Correlação entre Métricas')
    plt.tight_layout()
    plt.savefig(os.path.join('data', 'correlacao_heatmap.png'))
    plt.close()
    logging.info("✅ Mapa de calor salvo em data/correlacao_heatmap.png")

def remover_repositorios_clonados():
    repos_dir = os.path.join("C:\\ClonagemRepositorios", "repos")
    if os.path.exists(repos_dir):
        logging.info(f"🧹 Removendo repositórios clonados em: {repos_dir}")
        shutil.rmtree(repos_dir)
        logging.info("✅ Repositórios removidos com sucesso.")
    else:
        logging.info("📂 Nenhuma pasta de repositórios encontrada para remoção.")

def main():
    logging.info("🚀 Executando o script de análise de dados com métricas do CK...")
    try:
        input_file = verificar_arquivo_entrada()
        if input_file:
            analisar_dados(input_file)
        else:
            logging.info("❌ Nenhuma análise foi realizada, pois o arquivo de entrada está vazio.")
        logging.info("✅ Script de análise concluído.")
        remover_repositorios_clonados()
    except Exception as e:
        logging.error(f"❌ Erro durante a execução da análise: {e}")
        raise

if __name__ == "__main__":
    main()