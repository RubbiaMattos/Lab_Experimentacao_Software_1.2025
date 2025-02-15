"""
Análise de Repositórios Populares do GitHub

Este script coleta e analisa dados de repositórios populares do GitHub usando a API GraphQL
para responder questões sobre maturidade, contribuições externas, releases e tecnologias utilizadas.

Autores: Nataniel, Nelson e Rubia
Data: 16/02/2025
"""

# 🔹 Importação das bibliotecas necessárias
import os
import time
import requests
import traceback
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from datetime import datetime, UTC

# 🔹 Configuração do ambiente e carregamento do token do GitHub
def carregar_token():
    """Carrega o token do GitHub do arquivo `.env.config` e verifica sua validade."""

    # Definir caminho absoluto do `.env.config`
    env_path = os.path.abspath(".env.config")

    # Carregar variáveis do ambiente
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
    else:
        raise FileNotFoundError(f"❌ ERRO: Arquivo .env.config não encontrado em {env_path}")

    # Obter o token do ambiente
    token = os.getenv("GITHUB_TOKEN")

    # Validar o token
    if not token:
        raise ValueError("❌ ERRO: O token do GitHub não foi encontrado no arquivo .env.config")

    if not token.startswith("ghp_") or len(token) < 40:
        raise ValueError("❌ ERRO: Formato inválido do token. Verifique o arquivo .env.config")

    print("✅ Token carregado com sucesso!")
    return token


class GitHubDataCollector:
    """
    Classe responsável por coletar dados de repositórios populares do GitHub via API GraphQL.
    """

    def __init__(self, token):
        """Inicializa a conexão com a API do GitHub."""
        self.url = "https://api.github.com/graphql"
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }

    def execute_query(self, query, variables=None, max_retries=3, retry_delay=5):
        """
        Executa uma consulta GraphQL na API do GitHub, com tentativas de retry em caso de erro.
        """
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.url, json={'query': query, 'variables': variables},
                    headers=self.headers, timeout=30
                )

                if response.status_code == 200:
                    return response.json()

                elif response.status_code in [401, 403]:
                    raise Exception("❌ ERRO: Falha na autenticação. Token inválido ou expirado.")

                print(f"⚠️ Tentativa {attempt+1} falhou. Retentando em {retry_delay} segundos...")
                time.sleep(retry_delay)

            except requests.exceptions.RequestException as e:
                print(f"❌ Erro na requisição: {str(e)}")
                time.sleep(retry_delay)

        raise Exception("❌ Todas as tentativas de requisição falharam.")

    def get_top_repos(self, limit=100):
        """
        Coleta os repositórios mais populares do GitHub com base em estrelas (stars).
        """
        repos_data = []
        cursor = None

        query = """
        query($cursor: String) {
          search(query: "stars:>100 sort:stars-desc", type: REPOSITORY, first: 10, after: $cursor) {
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              nameWithOwner
              url
              stargazerCount
              primaryLanguage { name }
              createdAt
              updatedAt
              releases { totalCount }
              pullRequests(states: MERGED) { totalCount }
              issues(states: [OPEN, CLOSED]) { totalCount }
              closedIssues: issues(states: CLOSED) { totalCount }
            }
          }
        }
        """

        while len(repos_data) < limit:
            variables = {"cursor": cursor}
            result = self.execute_query(query, variables)

            if 'data' not in result:
                break

            search_data = result['data']['search']
            repos_data.extend(search_data['nodes'])

            if not search_data['pageInfo']['hasNextPage']:
                break

            cursor = search_data['pageInfo']['endCursor']
            time.sleep(2)

        return repos_data[:limit]


def analyze_data(repos_data):
    """
    Processa os dados coletados e calcula métricas para análise.
    """
    df = pd.DataFrame(repos_data)

    df['createdAt'] = pd.to_datetime(df['createdAt']).dt.tz_localize(None)
    df['updatedAt'] = pd.to_datetime(df['updatedAt']).dt.tz_localize(None)
    now = datetime.now(UTC)

    df['age_years'] = (now - df['createdAt']).dt.days / 365.25
    df['days_since_update'] = (now - df['updatedAt']).dt.days
    df['language'] = df['primaryLanguage'].apply(lambda x: x['name'] if x else 'Desconhecido')
    df['issues_closed_ratio'] = df.apply(
        lambda row: row['closedIssues']['totalCount'] / row['issues']['totalCount']
        if row['issues']['totalCount'] > 0 else 0,
        axis=1
    )

    return df


def generate_research_report(df):
    """
    Gera um relatório detalhado com base nos dados analisados.
    """
    print("\n📊 RELATÓRIO DE PESQUISA 📊")

    print("\n🔹 RQ 01: Sistemas populares são maduros?")
    print(f"Idade média: {df['age_years'].mean():.2f} anos")
    print(f"Idade mediana: {df['age_years'].median():.2f} anos")

    print("\n🔹 RQ 02: Sistemas populares recebem contribuições?")
    print(f"Média de PRs aceitas: {df['pullRequests'].apply(lambda x: x['totalCount']).mean():.2f}")

    print("\n🔹 RQ 03: Lançam releases com frequência?")
    print(f"Média de releases: {df['releases'].apply(lambda x: x['totalCount']).mean():.2f}")

    print("\n🔹 RQ 04: São atualizados com frequência?")
    print(f"Média de dias desde última atualização: {df['days_since_update'].mean():.2f}")

    print("\n🔹 RQ 05: Linguagens mais usadas:")
    top_languages = df['language'].value_counts().head(10)
    print(top_languages)

    # 🔹 Criar gráficos
    plt.figure(figsize=(10, 5))
    top_languages.plot(kind='bar', color='skyblue')
    plt.title("Top 10 Linguagens Mais Usadas")
    plt.xlabel("Linguagem")
    plt.ylabel("Número de Repositórios")
    plt.xticks(rotation=45)
    plt.savefig("top_languages.png", dpi=300, bbox_inches="tight")
    print("\n✅ Gráfico salvo como 'top_languages.png'")
    plt.show()


def main():
    """
    Função principal para coordenar todo o processo de coleta e análise.
    """
    try:
        token = carregar_token()
        collector = GitHubDataCollector(token)
        repos_data = collector.get_top_repos(100)

        if not repos_data:
            raise ValueError("Nenhum dado foi coletado")

        df = analyze_data(repos_data)
        generate_research_report(df)

        df.to_csv('github_analysis.csv', index=False)
        print("\n✅ Dados salvos em 'github_analysis.csv'")

    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
