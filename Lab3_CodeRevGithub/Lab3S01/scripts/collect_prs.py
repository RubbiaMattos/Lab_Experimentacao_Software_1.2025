import os
import json
import time
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime, timedelta
from github import Github, GithubException
from utils import get_github_token


def load_selected_repos(file_path):
    """
    Carrega a lista de repositórios selecionados a partir de um arquivo CSV.

    Args:
        file_path (str): Caminho para o arquivo CSV com os repositórios

    Returns:
        list: Lista com os nomes completos dos repositórios
    """
    df = pd.read_csv(file_path)
    return df["full_name"].tolist()


def collect_prs_from_repo(g, repo_name, max_prs=500):
    """
    Coleta PRs de um repositório.

    Args:
        g (Github): Instância autenticada da API do Github
        repo_name (str): Nome completo do repositório (formato: "dono/repo")
        max_prs (int): Número máximo de PRs a serem coletados por repositório

    Returns:
        list: Lista de dicionários com informações sobre os PRs coletados
    """
    print(f"Coletando PRs do repositório {repo_name}")
    collected_prs = []

    try:
        repo = g.get_repo(repo_name)

        # Buscar PRs fechados e mesclados (status CLOSED ou MERGED)
        pulls = repo.get_pulls(state="closed", sort="created", direction="desc")

        for pr in tqdm(pulls, total=min(pulls.totalCount, max_prs), desc=f"PRs de {repo_name}"):
            # Verifica se atingimos o limite máximo de PRs por repositório
            if len(collected_prs) >= max_prs:
                break

            try:
                # Pular PRs sem revisões
                reviews = list(pr.get_reviews())
                if len(reviews) == 0:
                    continue

                # Verifica se o PR foi fechado/mesclado pelo menos 1 hora após a criação
                created_at = pr.created_at
                closed_at = pr.closed_at

                if not closed_at:
                    continue

                time_diff = closed_at - created_at
                if time_diff < timedelta(hours=1):
                    continue

                # Coleta informações sobre o PR
                pr_info = {
                    "repo_name": repo_name,
                    "pr_number": pr.number,
                    "title": pr.title,
                    "body": pr.body,
                    "body_length": len(pr.body or ""),
                    "state": pr.state,
                    "merged": pr.merged,
                    "created_at": pr.created_at.isoformat(),
                    "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
                    "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                    "review_count": len(reviews),
                    "files_changed": pr.changed_files,
                    "additions": pr.additions,
                    "deletions": pr.deletions,
                    "comments": pr.comments,
                    "review_comments": pr.review_comments,
                    "time_to_close_hours": time_diff.total_seconds() / 3600
                }

                # Coleta informações sobre os participantes
                participants = set()
                participants.add(pr.user.login)

                # Adiciona revisores à lista de participantes
                for review in reviews:
                    if review.user and review.user.login:
                        participants.add(review.user.login)

                # Adiciona comentaristas à lista de participantes
                comments = list(pr.get_comments())
                for comment in comments:
                    if comment.user and comment.user.login:
                        participants.add(comment.user.login)

                # Adicionar participantes à informação do PR
                pr_info["participant_count"] = len(participants)

                collected_prs.append(pr_info)

            except GithubException as e:
                print(f"Erro ao processar PR #{pr.number} do repositório {repo_name}: {e}")
                # Se atingimos o limite de requisições da API, aguardamos o tempo necessário
                if e.status == 403 and 'rate limit' in str(e).lower():
                    handle_rate_limit(g)

    except GithubException as e:
        print(f"Erro ao acessar o repositório {repo_name}: {e}")
        # Se atingimos o limite de requisições da API, aguardamos o tempo necessário
        if e.status == 403 and 'rate limit' in str(e).lower():
            handle_rate_limit(g)

    return collected_prs


def handle_rate_limit(g):
    """
    Gerencia o limite de requisições da API do GitHub.

    Args:
        g (Github): Instância autenticada da API do Github
    """
    rate_limit = g.get_rate_limit()
    reset_time = rate_limit.core.reset.timestamp()
    current_time = datetime.now().timestamp()
    sleep_time = reset_time - current_time + 60  # +60 segundos para garantir

    if sleep_time > 0:
        print(f"Limite de requisições da API atingido. Aguardando {sleep_time / 60:.2f} minutos...")
        time.sleep(sleep_time)


def main():
    # Obter token do GitHub
    token = get_github_token()
    g = Github(token)

    # Criar diretório de dados se não existir
    os.makedirs("data", exist_ok=True)

    # Carregar repositórios selecionados
    selected_repos = load_selected_repos("data/selected_repos.csv")
    print(f"Encontrados {len(selected_repos)} repositórios para análise")

    # Coletar PRs de cada repositório
    all_prs = []

    for repo_name in selected_repos:
        repo_prs = collect_prs_from_repo(g, repo_name)
        all_prs.extend(repo_prs)

        # Salvar os dados coletados incrementalmente
        df = pd.DataFrame(all_prs)
        df.to_csv("data/collected_prs.csv", index=False)

        print(f"Total de PRs coletados até agora: {len(all_prs)}")

    print(f"Coleta concluída! Total de {len(all_prs)} PRs coletados de {len(selected_repos)} repositórios.")


if __name__ == "__main__":
    main()