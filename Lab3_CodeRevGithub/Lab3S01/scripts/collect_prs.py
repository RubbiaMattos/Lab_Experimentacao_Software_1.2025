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
    if not os.path.exists(file_path):
        print(f"Arquivo {file_path} não encontrado. Criando arquivo de exemplo...")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        example_repos = [
            {"full_name": "microsoft/vscode"},
            {"full_name": "facebook/react"},
            {"full_name": "torvalds/linux"},
        ]
        pd.DataFrame(example_repos).to_csv(file_path, index=False)
        print(f"Exemplo salvo em {file_path}")
    df = pd.read_csv(file_path)
    if "full_name" not in df.columns:
        raise ValueError(f"O arquivo {file_path} precisa da coluna 'full_name'")
    return df["full_name"].tolist()


def handle_rate_limit(g):
    try:
        rl = g.get_rate_limit().core
        wait_time = rl.reset.timestamp() - datetime.now().timestamp() + 60
        print(f"Aguardando {wait_time/60:.1f} minutos (rate limit)...")
        time.sleep(max(wait_time, 60))
    except Exception as e:
        print("Falha ao checar rate limit. Aguardando 10 minutos por segurança...")
        time.sleep(600)


def get_reviews_with_retry(pr, g, max_retries=3):
    delay = 1
    for attempt in range(max_retries):
        try:
            return list(pr.get_reviews())
        except GithubException as e:
            if e.status == 403:
                print(f"Erro 403 ao obter reviews do PR #{pr.number}. Tentativa {attempt+1}/{max_retries}")
                handle_rate_limit(g)
                time.sleep(delay)
                delay *= 2
            else:
                raise
    raise GithubException(f"Max retries exceeded para reviews do PR #{pr.number}")


def get_comments_with_retry(pr, g, max_retries=3):
    delay = 1
    for attempt in range(max_retries):
        try:
            try:
                return list(pr.get_issue_comments())
            except GithubException:
                # Em alguns casos pode ser necessário usar get_comments()
                return list(pr.get_comments())
        except GithubException as e:
            if e.status == 403:
                print(f"Erro 403 ao obter comentários do PR #{pr.number}. Tentativa {attempt+1}/{max_retries}")
                handle_rate_limit(g)
                time.sleep(delay)
                delay *= 2
            else:
                raise
    raise GithubException(f"Max retries exceeded para comentários do PR #{pr.number}")


def collect_prs_from_repo(g, repo_name, max_prs=500):
    collected = []
    try:
        repo = g.get_repo(repo_name)
        pulls = repo.get_pulls(state="closed", sort="created", direction="desc")

        for i, pr in enumerate(tqdm(pulls, desc=f"{repo_name}", total=max_prs)):
            if i >= max_prs:
                break

            try:
                # Obter reviews com retry
                reviews = get_reviews_with_retry(pr, g)
                if len(reviews) == 0:
                    continue

                if not pr.closed_at:
                    continue

                time_diff = pr.closed_at - pr.created_at
                if time_diff.total_seconds() < 3600:
                    continue

                # Coleta de participantes (autor, revisores e comentadores)
                participants = set()
                if pr.user and pr.user.login:
                    participants.add(pr.user.login)

                for review in reviews:
                    if review.user and review.user.login:
                        participants.add(review.user.login)

                # Obter comentários com retry
                comments = get_comments_with_retry(pr, g)
                for comment in comments:
                    if comment.user and comment.user.login:
                        participants.add(comment.user.login)

                collected.append({
                    "repo_name": repo_name,
                    "pr_number": pr.number,
                    "title": pr.title,
                    "body": pr.body or "",
                    "body_length": len(pr.body or ""),
                    "state": pr.state,
                    "merged": pr.merged,
                    "created_at": pr.created_at.isoformat(),
                    "closed_at": pr.closed_at.isoformat(),
                    "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                    "review_count": len(reviews),
                    "files_changed": pr.changed_files,
                    "additions": pr.additions,
                    "deletions": pr.deletions,
                    "comments": pr.comments,
                    "review_comments": pr.review_comments,
                    "time_to_close_hours": time_diff.total_seconds() / 3600,
                    "participant_count": len(participants)
                })

            except GithubException as e:
                if e.status == 403:
                    # Já tentou fazer o tratamento de rate limit dentro dos helpers
                    print(f"Pulando PR #{pr.number} devido a repetidos erros 403.")
                continue
            except Exception as e:
                print(f"Erro no PR #{pr.number}: {e}")
                continue

        return collected

    except GithubException as e:
        if e.status == 403:
            handle_rate_limit(g)
    except Exception as e:
        print(f"Erro geral ao acessar {repo_name}: {e}")
    return []


def save_prs_to_csv(prs, output_file):
    if prs:
        df = pd.DataFrame(prs)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"{len(prs)} PRs salvos em {output_file}")
    else:
        print("Nenhum PR para salvar.")


def main():
    token = get_github_token()
    g = Github(token, per_page=100)

    os.makedirs("data", exist_ok=True)
    repo_file = "data/selected_repos.csv"
    collected_file = "data/collected_prs.csv"

    selected_repos = load_selected_repos(repo_file)
    processed_repos = set()
    all_prs = []

    if os.path.exists(collected_file):
        df = pd.read_csv(collected_file)
        processed_repos = set(df["repo_name"].unique())
        all_prs = df.to_dict("records")

    to_process = [r for r in selected_repos if r not in processed_repos]
    print(f"{len(to_process)} repositórios restantes para coletar...")

    for i, repo_name in enumerate(to_process, 1):
        print(f"\n[{i}/{len(to_process)}] Coletando PRs de: {repo_name}")
        prs = collect_prs_from_repo(g, repo_name)
        if prs:
            all_prs.extend(prs)
            save_prs_to_csv(all_prs, collected_file)

    print(f"\n✅ Coleta concluída. Total de {len(all_prs)} PRs coletados.")


if __name__ == "__main__":
    main()

