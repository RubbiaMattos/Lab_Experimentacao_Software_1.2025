import pandas as pd
import os
# Faz a análise estatística dos resultados CSV
# Carrega os resultados

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos completos dos arquivos
RESULTS_FILE = os.path.join(BASE_DIR, "experiment_results.csv")
SUMMARY_FILE = os.path.join(BASE_DIR, "experiment_summary.csv")

df = pd.read_csv(RESULTS_FILE)

# Estatísticas descritivas por API
for api in df["API_Type"].unique():
    grp = df[df["API_Type"] == api]
    print(f"\n--- {api} ---")
    print("Tempo de Resposta (s):")
    print(grp["Response_Time"].describe())
    print("\nTamanho da Resposta (bytes):")
    print(grp["Response_Size"].describe())

# Salva resumo agregado
summary = df.groupby("API_Type").agg(
    Response_Time_mean=("Response_Time", "mean"),
    Response_Time_std =("Response_Time", "std"),
    Response_Size_mean =("Response_Size", "mean"),
    Response_Size_std  =("Response_Size", "std")
)
summary.to_csv(SUMMARY_FILE)

print(f"\n✅ Resumo salvo em '{os.path.basename(SUMMARY_FILE)}'.")
