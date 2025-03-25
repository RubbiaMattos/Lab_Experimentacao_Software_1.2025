import os
import json
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime


def get_github_token():
    token = "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"  # Insira seu token diretamente aqui
    if not token:
        raise ValueError("Token do GitHub não definido")
    return token



def fetch_popular_repos(token, count=200):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "q": "stars:>1000",
        "sort": "stars",
        "order": "desc",
        "per_page": 100
    }
    all_repos = []
    pages_to_fetch = (count + 99) // 100

    for page in tqdm(range(1, pages_to_fetch + 1), desc="Coletando repositórios"):
        params["page"] = page
        response = requests.get("https://api.github.com/search/repositories", headers=headers, params=params)
        if response.status_code != 200:
            print(f"Erro: {response.status_code}", response.json())
            break

        data = response.json()
        all_repos.extend(data.get("items", []))
    return all_repos[:count]

def filter_repos_with_min_prs(repos, token, min_prs=100):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    filtered = []
    for repo in tqdm(repos, desc="Filtrando por PRs"):
        full_name = repo["full_name"]
        url = f"https://api.github.com/search/issues?q=repo:{full_name}+is:pr+is:closed&per_page=1"
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            continue
        count = r.json().get("total_count", 0)
        if count >= min_prs:
            repo["pr_count"] = count
            filtered.append(repo)
    return filtered

def save_repos_to_csv(repos, file):
    selected = [
        "id", "full_name", "description", "language",
        "stargazers_count", "forks_count", "open_issues_count", "pr_count"
    ]
    rows = [{k: r.get(k) for k in selected} for r in repos]
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(file), exist_ok=True)
    df.to_csv(file, index=False)
    with open(file.replace(".csv", ".json"), "w") as f:
        json.dump(repos, f, indent=2)

def main():
    output_file = "data/selected_repos.csv"
    if os.path.exists(output_file):
        print(f"{output_file} já existe. Pulando coleta.")
        return
    token = get_github_token()
    repos = fetch_popular_repos(token)
    filtered = filter_repos_with_min_prs(repos, token)
    save_repos_to_csv(filtered, output_file)

if __name__ == "__main__":
    main()