"""
Análise de Repositórios Populares do GitHub

Este script realiza uma análise detalhada dos repositórios mais populares do GitHub,
coletando dados através da API GraphQL do GitHub e gerando relatórios estatísticos.

Autores:
    - Nataniel Geraldo Mendes Peixoto
    - Nelson de Campos Nolasco
    - Rubia Coelho de Matos


Data: 16 fevereiro/2025

Dependências:
    - pandas
    - requests
    - matplotlib
    - seaborn
"""
import time
import pandas as pd
import requests


class GitHubDataCollector:
    """
        Classe responsável pela coleta dos dados de repositórios do GitHub usando a API GraphQL.

        A classe utiliza a API GraphQL do GitHub para coletar informações detalhadas sobre
        os repositórios mais populares, incluindo estatísticas de stars, linguagens,
        contribuições e issues.

        Atributos:
            url (str): URL da API GraphQL do GitHub
            headers (dict): Cabeçalhos HTTP incluindo o token de autenticação
        """
    def __init__(self, token):
        """
                Inicializa o coletor com um token de autenticação do GitHub.

                Args:
                    token (str): Token de autenticação do GitHub para acesso à API
        """
        self.url = 'https://api.github.com/graphql'
        self.headers = {
            'Authorization': f'bearer {token}',
            'Content-Type': 'application/json',
        }

    def get_top_repos(self, limit=100):
        """
                Coleta dados dos repositórios mais populares do GitHub.

                Realiza consultas paginadas à API GraphQL do GitHub para coletar informações
                dos repositórios com mais de 100 stars.

                Args:
                    limit (int): Número máximo de repositórios a serem coletados (default: 100)

                Returns:
                    list: Lista de dicionários contendo dados dos repositórios

                Raises:
                    Exception: Se houver erro na comunicação com a API ou no processamento dos dados
        """

        query = """
        query($cursor: String) {
          search(query: "stars:>100", type: REPOSITORY, first: 25, after: $cursor) {
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              ... on Repository {
                nameWithOwner
                url
                stargazerCount
                primaryLanguage {
                  name
                }
                createdAt
                updatedAt
                defaultBranchRef {
                  name
                }
                releases {
                  totalCount
                }
                pullRequests(states: MERGED) {
                  totalCount
                }
                issues(states: [OPEN, CLOSED]) {
                  totalCount
                }
                closedIssues: issues(states: CLOSED) {
                  totalCount
                }
              }
            }
          }
        }
        """

        repos_data = []
        cursor = None

        print("\nIniciando coleta de repositórios...")

        while len(repos_data) < limit:
            try:
                variables = {"cursor": cursor}
                response = requests.post(
                    self.url,
                    headers=self.headers,
                    json={'query': query, 'variables': variables}
                )

                print(f"Status da resposta: {response.status_code}")

                if response.status_code != 200:
                    print(f"Erro na requisição: {response.text}")
                    break

                result = response.json()

                if 'errors' in result:
                    print(f"Erros GraphQL: {result['errors']}")
                    break

                if 'data' not in result:
                    print(f"Resposta sem dados: {result}")
                    break

                current_repos = result['data']['search']['nodes']
                if not current_repos:
                    break

                repos_data.extend(current_repos)
                print(f"Repositórios coletados até agora: {len(repos_data)}")

                page_info = result['data']['search']['pageInfo']
                if not page_info['hasNextPage']:
                    break

                cursor = page_info['endCursor']
                time.sleep(2)  # Respeitar limite de taxa

            except Exception as e:
                print(f"Erro durante a coleta: {str(e)}")
                print(f"Resposta completa: {response.text if 'response' in locals() else 'No response'}")
                break

        return repos_data[:limit]


def analyze_data(repos_data):
    """
        Analisa os dados coletados dos repositórios, calculando métricas solicitadas.

        Processa os dados brutos dos repositórios, calculando métricas derivadas como
        idade do repositório, tempo desde última atualização e taxa de resolução de issues.

        Args:
            repos_data (list): Lista de dicionários com dados dos repositórios

        Returns:
            pandas.DataFrame: DataFrame contendo os dados analisados e métricas calculadas
    """
    # Converte para DataFrame
    df = pd.DataFrame(repos_data)

    # Converte as datas para UTC
    df['createdAt'] = pd.to_datetime(df['createdAt']).dt.tz_convert('UTC')
    df['updatedAt'] = pd.to_datetime(df['updatedAt']).dt.tz_convert('UTC')
    now = pd.Timestamp.now(tz='UTC')

    # Calcula métricas
    df['age_days'] = (now - df['createdAt']).dt.total_seconds() / (24 * 60 * 60)
    df['days_since_update'] = (now - df['updatedAt']).dt.total_seconds() / (24 * 60 * 60)
    df['language'] = df['primaryLanguage'].apply(lambda x: x['name'] if x else 'None')

    # Calcula razão de issues fechadas
    df['issues_closed_ratio'] = df.apply(
        lambda row: row['closedIssues']['totalCount'] / row['issues']['totalCount']
        if row['issues']['totalCount'] > 0 else 0,
        axis=1
    )

    return df


def generate_research_report(df):
    """
        Gera um relatório de pesquisa detalhado com base nos dados analisados.

        Limpa os NONE que apareceram numa primeira pesquisa para se ter resultados mais
        próximos do que é pedido
        Analisa diferentes aspectos dos repositórios populares por meio de questions de
        pesquisa (RQs) específicas, gerando visualizações e métricas estatísticas.

        Args:
            df (pandas.DataFrame): DataFrame contendo os dados analisados

        Outputs:
            - Imprime resultados estatísticos na tela
            - Gera e salva gráfico de barras das linguagens mais populares
            - Fornece análises detalhadas para cada RQ
    """
    print("\nRESULTADOS DA PESQUISA:")

    # RQ 01
    print("\nRQ 01. Sistemas populares são maduros/antigos?")
    idade_media = df['age_days'].mean() / 365.25
    idade_mediana = df['age_days'].median() / 365.25
    print(f"Idade média dos repositórios: {idade_media:.2f} anos")
    print(f"Mediana da idade: {idade_mediana:.2f} anos")

    # RQ 02

    print("\nRQ 02. Sistemas populares recebem muita contribuição externa?")
    try:
        prs_mean = df['pullRequests'].apply(lambda x: x['totalCount']).mean()
        prs_median = df['pullRequests'].apply(lambda x: x['totalCount']).median()
        print(f"Média de PRs aceitas: {prs_mean:.2f}")
        print(f"Mediana de PRs aceitas: {prs_median:.2f}")

        import seaborn as sns
        import matplotlib.pyplot as plt

        # Extrai a contagem de PRs aceitos
        df['pr_count'] = df['pullRequests'].apply(lambda x: x['totalCount'])

        # Configuração do gráfico
        plt.figure(figsize=(8, 6))
        sns.boxplot(y=df['pr_count'], color="skyblue")

        # Títulos e rótulos
        plt.title("Distribuição do Número de PRs Aceitos", fontsize=14)
        plt.ylabel("Quantidade de PRs Aceitos")

        # Salva o gráfico
        plt.savefig('qtd_PRs_aceitos.png', dpi=300, bbox_inches='tight')
        print("\nGráfico salvo como 'qtd_PRs_aceitos.png'")

        # Mostra o gráfico no PyCharm Professional (no Community talvez tenha que baixar plugin)
        plt.show()

        # Fecha a figura para liberar memória
        plt.close()

    except Exception as e:
        print(f"\nErro ao gerar o gráfico: {str(e)}")
        import traceback
        print(traceback.format_exc())

    # RQ 03
    print("\nRQ 03. Sistemas populares lançam releases com frequência?")
    releases_mean = df['releases'].apply(lambda x: x['totalCount']).mean()
    releases_median = df['releases'].apply(lambda x: x['totalCount']).median()
    print(f"Média de releases: {releases_mean:.2f}")
    print(f"Mediana de releases: {releases_median:.2f}")

    # RQ 04
    print("\nRQ 04. Sistemas populares são atualizados com frequência?")
    update_mean = df['days_since_update'].mean()
    update_median = df['days_since_update'].median()
    print(f"Média de dias desde última atualização: {update_mean:.2f}")
    print(f"Mediana de dias desde última atualização: {update_median:.2f}")

    # RQ 05
    print("\nRQ 05. Sistemas populares são escritos nas linguagens mais populares?")
    try:
        # Configurar o matplotlib especificamente para o PyCharm, IDE usada pelo grupo
        import matplotlib
        matplotlib.use('module://backend_interagg')  # Backend específico para IDEs
        import matplotlib.pyplot as plt
        import seaborn as sns

        # Limpa os None e prepara os dados
        languages_count = df['language'].replace('None', pd.NA).dropna().value_counts().head(10)

        print("\nTop 10 linguagens mais usadas nos repositórios populares:")
        print(languages_count)

        # Cria nova figura com tamanho específico para o PyCharm, IDE utilizada
        plt.figure(figsize=(10, 6), dpi=100)

        # Cria o plot usando Seaborn
        ax = sns.barplot(
            x=languages_count.index,
            y=languages_count.values,
            hue=languages_count.index,
            palette='husl',
            legend=False
        )

        # Configura o gráfico
        plt.title('Top 10 Linguagens de Programação mais Populares no GitHub')
        plt.xlabel('Linguagens')
        plt.ylabel('Número de Repositórios')

        # Rotaciona labels
        plt.xticks(rotation=45, ha='right')

        # Adiciona valores nas barras
        for i, v in enumerate(languages_count.values):
            ax.text(i, v, str(int(v)), ha='center', va='bottom')

        # Ajusta layout
        plt.tight_layout()

        # Salva o gráfico
        plt.savefig('top_languages.png', dpi=300, bbox_inches='tight')
        print("\nGráfico salvo como 'top_languages.png'")

        # Mostra o gráfico no PyCharm Professional (no Community talvez tenha que baixar plugin)
        plt.show()

        # Fecha a figura para liberar memória
        plt.close()

    except Exception as e:
        print(f"\nErro ao gerar o gráfico: {str(e)}")
        import traceback
        print(traceback.format_exc())

    # RQ 06
    print("\nRQ 06. Sistemas populares possuem um alto percentual de issues fechadas?")
    issues_ratio_mean = df['issues_closed_ratio'].mean() * 100
    issues_ratio_median = df['issues_closed_ratio'].median() * 100
    print(f"Média do percentual de issues fechadas: {issues_ratio_mean:.2f}%")
    print(f"Mediana do percentual de issues fechadas: {issues_ratio_median:.2f}%")

    # RQ 07
    print("\nRQ 07. Análise por linguagem das principais métricas:")
    top_languages = languages_count.index.tolist()

    metrics_by_language = df[df['language'].isin(top_languages)].groupby('language').agg({
        'pullRequests': lambda x: pd.Series([i['totalCount'] for i in x]).mean(),
        'releases': lambda x: pd.Series([i['totalCount'] for i in x]).mean(),
        'days_since_update': 'mean'
    }).round(2)

    print("\nMédia de métricas por linguagem popular:")
    print(metrics_by_language)


def main():
    """
        Função principal que coordena todo o processo de coleta, análise e geração de relatório.

        Fluxo de execução:
        1. Inicializa conexão com API do GitHub
        2. Coleta dados dos repositórios mais populares
        3. Processa e analisa os dados coletados
        4. Gera relatório com visualizações e métricas
        5. Salva resultados em arquivo CSV

        Raises:
            ValueError: Se nenhum dado for coletado
            Exception: Para outros erros durante a execução
    """
    try:
        # Substitua com seu token do GitHub
        token = "ghp_TOKEN GITHUB" #<-------- Token do Github aqui

        print("Iniciando coleta de dados...")
        collector = GitHubDataCollector(token)
        repos_data = collector.get_top_repos(100)

        if not repos_data:
            raise ValueError("Nenhum dado foi coletado")

        print(f"\nTotal de repositórios coletados: {len(repos_data)}")

        print("\nAnalisando os dados...")
        df = analyze_data(repos_data)

        print("\nGerando relatório...")
        generate_research_report(df)

        df.to_csv('github_analysis.csv', index=False)
        print("\nDados salvos em 'github_analysis.csv'")

    except Exception as e:
        print(f"Erro: {str(e)}")
        raise


if __name__ == "__main__":
    main()