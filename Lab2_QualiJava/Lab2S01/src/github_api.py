import requests
import pandas as pd

GITHUB_API_URL = "https://api.github.com"
HEADERS = {"Authorization": "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"} # <-- Token Github aqui

def fetch_top_repositories(language, max_repos=100):
    """
    Coleta os repositórios mais populares de uma linguagem específica.
    """
    repos = []
    page = 1

    while len(repos) < max_repos:
        url = f"{GITHUB_API_URL}/search/repositories"
        params = {"q": f"language:{language}", "sort": "stars", "order": "desc", "per_page": 100, "page": page}
        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code != 200:
            print(f"Erro na requisição: {response.status_code}")
            break

        data = response.json()["items"]
        repos.extend(data)

        if len(data) < 100:
            break

        page += 1

    df = pd.DataFrame([{
        "repo_name": repo["name"],
        "repo_url": repo["html_url"],
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "created_at": repo["created_at"]
    } for repo in repos[:max_repos]])

    return df

if __name__ == "__main__":
    repos = fetch_top_repositories(language="Java")
    repos.to_csv("data/raw/top_java_repositories.csv", index=False)