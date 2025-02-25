import pandas as pd
from scipy.stats import spearmanr

def correlation_analysis(data):
    """
    Realiza análise de correlação entre as métricas.
    """
    correlations = {}
    for col in ["stars", "CBO_mean", "DIT_mean", "LCOM_mean"]:
        if col != "stars":
            corr, p_value = spearmanr(data["stars"], data[col])
            correlations[col] = {"correlation": corr, "p_value": p_value}

    return pd.DataFrame(correlations).T

if __name__ == "__main__":
    DATA_PATH = "data/results/summary.csv"
    data = pd.read_csv(DATA_PATH)
    correlations = correlation_analysis(data)
    correlations.to_csv("data/results/correlations.csv")