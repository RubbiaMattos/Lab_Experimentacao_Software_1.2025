import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

# Diretórios e leitura dos dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPH_DIR = os.path.join(BASE_DIR, "Gráficos")
os.makedirs(GRAPH_DIR, exist_ok=True)

CSV_PATH = os.path.join(BASE_DIR, "experiment_results.csv")
df = pd.read_csv(CSV_PATH)

# Histograma para Response_Time
def plot_hist(col, title, xlabel, out_file):
    plt.figure()
    for api in df["API_Type"].unique():
        subset = df[df["API_Type"] == api]
        plt.hist(subset[col], bins=10, alpha=0.5, label=api)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Frequência")
    plt.legend()
    output_path = os.path.join(GRAPH_DIR, out_file)
    plt.savefig(output_path)
    plt.close()
    print(f"✅ Gráfico salvo: {output_path}")

# Gráfico de barras para Response_Size
def plot_bar_response_size(out_file):
    df_means = df.groupby("API_Type")["Response_Size"].mean()

    plt.figure()
    df_means.plot(kind="bar", color=["skyblue", "orange"])
    plt.title("Tamanho Médio da Resposta por Tipo de API")
    plt.ylabel("Tamanho da Resposta (bytes)")
    plt.xlabel("Tipo de API")
    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = os.path.join(GRAPH_DIR, out_file)
    plt.savefig(output_path)
    plt.close()
    print(f"✅ Gráfico salvo: {output_path}")

# Execução principal
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

    plot_bar_response_size(args.size_out)