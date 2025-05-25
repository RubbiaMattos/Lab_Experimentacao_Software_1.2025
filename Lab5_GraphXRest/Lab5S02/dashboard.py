import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Gera os histogramas de tempo e tamanho de resposta
# Leitura
df = pd.read_csv("experiment_results.csv")

def plot_hist(col, title, xlabel, out_file):
    plt.figure()
    for api in df["API_Type"].unique():
        subset = df[df["API_Type"] == api]
        plt.hist(subset[col], bins=10, alpha=0.5, label=api)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Frequência")
    plt.legend()
    plt.savefig(out_file)
    plt.close()
    print(f"✅ Gráfico salvo: {out_file}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--time-out", default="response_time_distribution.png")
    p.add_argument("--size-out", default="response_size_distribution.png")
    args = p.parse_args()

    plot_hist(
        "Response_Time",
        "Distribuição do Tempo de Resposta (GitHub API)",
        "Tempo (s)",
        args.time_out
    )
    plot_hist(
        "Response_Size",
        "Distribuição do Tamanho da Resposta (GitHub API)",
        "Tamanho (bytes)",
        args.size_out
    )
