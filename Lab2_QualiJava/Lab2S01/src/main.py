from github_api import fetch_top_repositories
from ck_runner import run_ck_tool
from data_processing import summarize_metrics
from analysis import correlation_analysis
from visualization import plot_correlations

if __name__ == "__main__":
    # 1. Coleta de repositórios
    repos = fetch_top_repositories(language="Java")
    repos.to_csv("data/raw/top_java_repositories.csv", index=False)

    # 2. Clonagem de repositórios e execução do CK
    # (Assume-se que os repositórios foram clonados manualmente ou por script)

    # 3. Processamento e sumarização
    summary = summarize_metrics("data/processed/metrics")
    summary.to_csv("data/results/summary.csv", index=False)

    # 4. Análise de correlações
    correlations = correlation_analysis(summary)
    correlations.to_csv("data/results/correlations.csv")

    # 5. Visualização
    plot_correlations(summary)