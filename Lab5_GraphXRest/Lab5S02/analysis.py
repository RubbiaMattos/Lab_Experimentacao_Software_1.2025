import pandas as pd
# faz a análise estatística dos resultados CSV
# Carrega os resultados
df = pd.read_csv("experiment_results.csv")

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
summary.to_csv("experiment_summary.csv")
print("\n✅ Resumo salvo em 'experiment_summary.csv'.")
