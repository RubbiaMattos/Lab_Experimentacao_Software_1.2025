import os
import subprocess
import pandas as pd

def clone_repositories(repo_list_path, output_dir):
    """
    Clona os repositórios listados em um arquivo CSV.
    """
    os.makedirs(output_dir, exist_ok=True)
    repos = pd.read_csv(repo_list_path)

    for _, row in repos.iterrows():
        repo_url = row['repo_url']
        repo_name = repo_url.split('/')[-1]
        repo_path = os.path.join(output_dir, repo_name)

        if not os.path.exists(repo_path):
            print(f"Clonando {repo_url}...")
            subprocess.run(["git", "clone", repo_url, repo_path])

if __name__ == "__main__":
    INPUT_CSV = "data/raw/top_java_repositories.csv"
    OUTPUT_DIR = "data/raw/repositories"
    clone_repositories(INPUT_CSV, OUTPUT_DIR)