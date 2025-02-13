"""
Análise de Repositórios Populares do GitHub
Este script coleta e analisa dados de repositórios populares do GitHub para responder
questões de pesquisa do Lab. Exper. Software sobre maturidade, contribuições, releases
e tecnologias utilizadas.

Questões de Pesquisa:
RQ 01. Sistemas populares são maduros/antigos?
RQ 02. Sistemas populares recebem muita contribuição externa?
RQ 03. Sistemas populares lançam releases com frequência?
RQ 04. Sistemas populares são atualizados com frequência?
RQ 05. Sistemas populares são escritos nas linguagens mais populares?
RQ 06. Sistemas populares possuem um alto percentual de issues fechadas?

Autores: [Nataniel, Nelson e Rubia]
Data: [16/02/2025]
"""

# Importação das bibliotecas necessárias
import os
from datetime import datetime, timedelta
import pandas as pd
import requests
import matplotlib.pyplot as plt
import time
from collections import Counter


class GitHubDataCollector:
    """
        Classe responsável por coletar dados da API GraphQL do GitHub.

        Attributes:
            headers (dict): Cabeçalhos HTTP incluindo o token de autenticação
            url (str): URL base da API GraphQL do GitHub
    """

    def __init__(self, token):
        """
                Inicializa o coletor com um token de autenticação do GitHub.

                Args:
                    token (str): Token de autenticação do GitHub

                Raises:
                    ValueError: Se o token for inválido ou muito curto
        """
        self.headers = {"Authorization": f"Bearer {token}"}
        self.url = "https://api.github.com/graphql"

        if not token or len(token) < 40:
            raise ValueError("Token inválido: muito curto ou vazio")
        print(f"Token configurado (primeiros 5 caracteres): {token[:5]}...")

    def execute_query(self, query, variables=None, max_retries=3, retry_delay=5):
        """
               Executa uma consulta GraphQL na API do GitHub com retry automático.

               Args:
                   query (str): Consulta GraphQL
                   variables (dict, optional): Variáveis da consulta
                   max_retries (int): Número máximo de tentativas
                   retry_delay (int): Tempo de espera entre tentativas em segundos

               Returns:
                   dict: Resposta da API em formato JSON

               Raises:
                   Exception: Se todas as tentativas falharem
        """
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.url,
                    json={'query': query, 'variables': variables},
                    headers=self.headers,
                    timeout=30
                )

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 502:
                    if attempt < max_retries - 1:
                        print(f"Erro 502. Tentativa {attempt + 1} de {max_retries}")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue

                raise Exception(f"Erro na consulta: {response.status_code}")

            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"Erro na requisição. Tentativa {attempt + 1} de {max_retries}")
                    time.sleep(retry_delay)
                    continue
                raise

    def get_top_repos(self, limit=1000):
        """
                Coleta dados dos repositórios mais populares do GitHub.

                Args:
                    limit (int): Número máximo de repositórios a serem coletados

                Returns:
                    list: Lista de dicionários com dados dos repositórios

                Raises:
                    Exception: Se houver erro durante a coleta dos dados
        """
        repos_data = []
        cursor = None

        query = """
        query($cursor: String) {
          search(query: "stars:>100 sort:stars-desc", type: REPOSITORY, first: 25, after: $cursor) {
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              ... on Repository {
                nameWithOwner
                stargazerCount
                forkCount
                primaryLanguage {
                  name
                }
                createdAt
                updatedAt
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
                defaultBranchRef {
                  target {
                    ... on Commit {
                      history {
                        totalCount
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """

        while len(repos_data) < limit:
            try:
                variables = {"cursor": cursor}
                result = self.execute_query(query, variables)

                if not result or 'data' not in result:
                    break

                search_data = result['data']['search']
                current_repos = [repo for repo in search_data['nodes'] if repo]
                repos_data.extend(current_repos)

                print(f"Coletados {len(repos_data)} repositórios de {limit}")

                if not search_data['pageInfo']['hasNextPage']:
                    break

                cursor = search_data['pageInfo']['endCursor']
                time.sleep(2)

            except Exception as e:
                print(f"Erro durante a coleta: {str(e)}")
                break

        return repos_data[:limit]


def analyze_data(repos_data):
    """
        Analisa os dados coletados dos repositórios, calculando métricas relevantes.

        Args:
            repos_data (list): Lista de dicionários com dados dos repositórios

        Returns:
            pandas.DataFrame: DataFrame contendo as métricas calculadas

        Raises:
            ValueError: Se não houver dados válidos para análise
        """
    try:
        valid_data = []
        current_date = pd.Timestamp.now(tz='UTC')

        for repo in repos_data:
            if not repo:
                continue

            try:
                # Convertendo datas de forma mais segura
                created_at = pd.to_datetime(repo.get('createdAt'))
                updated_at = pd.to_datetime(repo.get('updatedAt'))

                # Se as datas já têm timezone, usa tz_convert, senão usa tz_localize
                if created_at.tz is None:
                    created_at = created_at.tz_localize('UTC')
                if updated_at.tz is None:
                    updated_at = updated_at.tz_localize('UTC')

                # Cálculos para as requisições RQs
                age_years = (current_date - created_at).total_seconds() / (365.25 * 24 * 60 * 60)
                days_since_update = (current_date - updated_at).total_seconds() / (24 * 60 * 60)

                # Processando os dados de issues
                total_issues = repo.get('issues', {}).get('totalCount', 0)
                closed_issues = repo.get('closedIssues', {}).get('totalCount', 0)
                issues_ratio = closed_issues / total_issues if total_issues > 0 else 0

                # Criando dicionário de dados
                repo_data = {
                    'repo': repo.get('nameWithOwner', 'N/A'),
                    'stars': int(repo.get('stargazerCount', 0)),
                    'language': repo.get('primaryLanguage', {}).get('name', 'Não especificada') if repo.get(
                        'primaryLanguage') else 'Não especificada',
                    'age_years': round(age_years, 2),
                    'merged_prs': int(repo.get('pullRequests', {}).get('totalCount', 0)),
                    'releases': int(repo.get('releases', {}).get('totalCount', 0)),
                    'days_since_update': round(days_since_update, 2),
                    'total_issues': total_issues,
                    'closed_issues': closed_issues,
                    'issues_ratio': round(issues_ratio, 4)
                }

                # Validação básica dos dados
                if repo_data['age_years'] >= 0 and repo_data['days_since_update'] >= 0:
                    valid_data.append(repo_data)
                else:
                    print(f"Dados inválidos para o repositório {repo_data['repo']}")

            except Exception as e:
                print(f"Erro ao processar repositório {repo.get('nameWithOwner', 'N/A')}: {str(e)}")
                continue

        if not valid_data:
            raise ValueError("Nenhum dado válido para análise")

        # Criando DataFrame
        df = pd.DataFrame(valid_data)

        # Convertendo tipos de dados
        numeric_columns = ['age_years', 'merged_prs', 'releases', 'days_since_update',
                           'total_issues', 'closed_issues', 'issues_ratio', 'stars']

        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Verificação final
        if df.empty:
            raise ValueError("DataFrame vazio após processamento")

        print(f"Processados com sucesso {len(df)} repositórios")
        return df

    except Exception as e:
        print(f"Erro na análise dos dados: {str(e)}")
        raise


def generate_research_report(df):
    """
        Gera um relatório de pesquisa com base nas análises dos dados coletados.

        Args:
            df (pandas.DataFrame): DataFrame contendo os dados analisados dos repositórios

        Raises:
            ValueError: Se houver colunas necessárias ausentes no DataFrame
            Exception: Para outros erros durante a geração do relatório

        Returns:
            None: Imprime o relatório e gera visualizações gráficas
        """
    try:
        print("\n=== RELATÓRIO DE PESQUISA ===\n")

        # Verificando se todas as colunas necessárias existem
        required_columns = ['age_years', 'merged_prs', 'releases', 'days_since_update',
                            'language', 'issues_ratio', 'total_issues', 'closed_issues']

        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Colunas ausentes no DataFrame: {missing_columns}")

        # RQ 01: Maturidade dos sistemas
        print("RQ 01: Sistemas populares são maduros/antigos?")
        print(f"Mediana de idade: {df['age_years'].median():.2f} anos")
        print(f"Média de idade: {df['age_years'].mean():.2f} anos")
        print(f"Repos com mais de 5 anos: {(df['age_years'] > 5).mean() * 100:.1f}%")

        plt.figure(figsize=(10, 6))
        plt.hist(df['age_years'].dropna(), bins=20)
        plt.title('Distribuição da Idade dos Repositórios')
        plt.xlabel('Idade (anos)')
        plt.ylabel('Número de Repositórios')
        plt.show()

        # RQ 02: Contribuição externa
        print("\nRQ 02: Sistemas populares recebem muita contribuição externa?")
        print(f"Mediana de Pull Request (PRs) aceitas: {df['merged_prs'].median():.0f}")
        print(f"Média de PRs aceitas: {df['merged_prs'].mean():.0f}")

        # RQ 03: Frequência de releases
        print("\nRQ 03: Sistemas populares lançam releases com frequência?")
        print(f"Mediana de releases: {df['releases'].median():.0f}")
        print(f"Média de releases: {df['releases'].mean():.0f}")

        # RQ 04: Frequência de atualizações
        print("\nRQ 04: Sistemas populares são atualizados com frequência?")
        print(f"Mediana de dias desde última atualização: {df['days_since_update'].median():.0f}")
        print(f"Média de dias desde última atualização: {df['days_since_update'].mean():.0f}")

        # RQ 05: Linguagens populares
        print("\nRQ 05: Sistemas populares são escritos nas linguagens mais populares?")
        top_languages = df['language'].value_counts().head(10)
        print("\nTop 10 Linguagens:")
        print(top_languages)

        plt.figure(figsize=(12, 6))
        top_languages.plot(kind='bar')
        plt.title('Top 10 Linguagens Mais Usadas')
        plt.xlabel('Linguagem')
        plt.ylabel('Número de Repositórios')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # RQ 06: Issues fechadas
        print("\nRQ 06: Sistemas populares possuem um alto percentual de issues fechadas?")
        print(f"Mediana da taxa de issues fechadas: {df['issues_ratio'].median() * 100:.1f}%")
        print(f"Média da taxa de issues fechadas: {df['issues_ratio'].mean() * 100:.1f}%")

        def generate_research_report(df):

            try:
                # [código anterior permanece igual até RQ 06]

                # RQ 07: Análise por Linguagem
                print("\nRQ 07: Sistemas escritos em linguagens mais populares recebem mais contribuição externa,")
                print("lançam mais releases e são atualizados com mais frequência?\n")

                # Seleciona top 5 linguagens mais populares
                top_langs = df['language'].value_counts().head(5).index.tolist()

                # Filtra apenas repositórios das top 5 linguagens
                df_top_langs = df[df['language'].isin(top_langs)]

                # Calcula métricas por linguagem
                metrics_by_lang = df_top_langs.groupby('language').agg({
                    'merged_prs': ['median', 'mean'],
                    'releases': ['median', 'mean'],
                    'days_since_update': ['median', 'mean']
                }).round(2)

                # Renomeia as colunas para melhor legibilidade
                metrics_by_lang.columns = [
                    'PRs (mediana)', 'PRs (média)',
                    'Releases (mediana)', 'Releases (média)',
                    'Dias desde update (mediana)', 'Dias desde update (média)'
                ]

                print("Análise por Linguagem:")
                print(metrics_by_lang)

                # Visualizações para RQ 07
                fig, axes = plt.subplots(1, 3, figsize=(18, 6))

                # Gráfico de PRs por linguagem
                df_top_langs.boxplot(column='merged_prs', by='language', ax=axes[0])
                axes[0].set_title('PRs Aceitas por Linguagem')
                axes[0].set_ylabel('Número de PRs')
                axes[0].tick_params(axis='x', rotation=45)

                # Gráfico de releases por linguagem
                df_top_langs.boxplot(column='releases', by='language', ax=axes[1])
                axes[1].set_title('Releases por Linguagem')
                axes[1].set_ylabel('Número de Releases')
                axes[1].tick_params(axis='x', rotation=45)

                # Gráfico de tempo desde última atualização por linguagem
                df_top_langs.boxplot(column='days_since_update', by='language', ax=axes[2])
                axes[2].set_title('Dias Desde Última Atualização')
                axes[2].set_ylabel('Dias')
                axes[2].tick_params(axis='x', rotation=45)

                plt.tight_layout()
                plt.show()

                # Análise estatística adicional
                print("\nMétricas adicionais por linguagem:")
                for lang in top_langs:
                    repos_lang = df_top_langs[df_top_langs['language'] == lang]
                    print(f"\n{lang}:")
                    print(f"Número de repositórios: {len(repos_lang)}")
                    print(
                        f"Média de PRs por mês: {(repos_lang['merged_prs'] / repos_lang['age_years'] / 12).mean():.1f}")
                    print(f"Média de releases por ano: {(repos_lang['releases'] / repos_lang['age_years']).mean():.1f}")

                # [resto do código permanece igual]

            except Exception as e:
                print(f"Erro no relatório: {str(e)}")
                raise

        # Conclusões gerais
        print("\n=== CONCLUSÕES GERAIS ===")
        print("\nCom base nos dados aqui analisados:")
        print(f"1. A maioria dos repositórios populares são maduros (mediana de {df['age_years'].median():.1f} anos)")
        print(f"2. Há uma média de {df['merged_prs'].mean():.0f} Pull Requests (PRs) aceitas por repositório")
        print(f"3. Repositórios populares lançam em média {df['releases'].mean():.0f} releases")
        print(f"4. A última atualização ocorre em média a cada {df['days_since_update'].median():.0f} dias")
        print(f"5. {top_languages.index[0]} é a linguagem mais comum entre repositórios populares")
        print(f"6. Em média, {df['issues_ratio'].mean() * 100:.1f}% das issues são fechadas")

    except Exception as e:
        print(f"Erro no relatório: {str(e)}")
        raise


def main():
    """
        Função principal que comanda a execução do programa.

        Esta função:
        1. Configura o token de autenticação
        2. Inicializa o coletor de dados
        3. Coleta os dados dos repositórios
        4. Analisa os dados coletados
        5. Gera o relatório de pesquisa

        Raises:
            ValueError: Se o token for inválido
            Exception: Para outros erros durante a execução
        """
    try:
        token = os.getenv('GITHUB_TOKEN', 'ghp_TOKEN') #Inserir o Token Github aqui

        if not token.startswith('ghp_'):
            raise ValueError("Token inválido")

        collector = GitHubDataCollector(token)
        print("Coletando os dados dos repositórios...")
        repos_data = collector.get_top_repos()

        if not repos_data:
            raise ValueError("Nenhum dado foi coletado")

        print("Analisando os dados...")
        df = analyze_data(repos_data)

        generate_research_report(df)

        # Salvando dados
        df.to_csv('github_analysis.csv', index=False)
        print("\nDados salvos em 'github_analysis.csv'")

    except Exception as e:
        print(f"Erro: {str(e)}")
        raise


if __name__ == "__main__":
    main()
