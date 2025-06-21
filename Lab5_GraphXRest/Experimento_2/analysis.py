import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import os

# Caminho do CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "experiment_graphql_incremental.csv")
df = pd.read_csv(CSV_PATH)

# Extrai número do Trial_Name (1 a 10)
df["Query_Level"] = df["Trial_Name"].str.extract(r'(\d+)').astype(int)

# Agrupa por nível lógico da query (1campos a 10campos)
grouped = df.groupby("Query_Level").agg({
    "Response_Time": ["mean", "std"],
    "Response_Size": ["mean", "std"]
}).reset_index()
grouped.columns = ["Query_Level", "Time_Mean", "Time_Std", "Size_Mean", "Size_Std"]

# Correlação de Spearman com Query_Level
spearman_time = spearmanr(df["Query_Level"], df["Response_Time"])
spearman_size = spearmanr(df["Query_Level"], df["Response_Size"])

# Impressão no terminal
print(f"📈 Correlação (Query_Level vs Tempo): ρ = {spearman_time.correlation:.4f}, p = {spearman_time.pvalue:.4g}")
print(f"📦 Correlação (Query_Level vs Tamanho): ρ = {spearman_size.correlation:.4f}, p = {spearman_size.pvalue:.4g}")

# Diretório de gráficos
GRAPH_DIR = os.path.join(BASE_DIR, "Graficos_Incremental")
os.makedirs(GRAPH_DIR, exist_ok=True)

# Gráfico Tempo
plt.figure()
plt.errorbar(grouped["Query_Level"], grouped["Time_Mean"], yerr=grouped["Time_Std"], fmt='-o', color='blue')
plt.xticks(grouped["Query_Level"])  # Garante ordem correta
plt.xlabel("Nível Lógico da Query (Trial_Name)")
plt.ylabel("Tempo Médio de Resposta (s)")
plt.title("Tempo de Resposta vs Complexidade Lógica da Query")
plt.grid(True)
plt.text(
    0.95, 0.05,
    f"ρ = {spearman_time.correlation:.3f}\np = {spearman_time.pvalue:.4f}",
    transform=plt.gca().transAxes,
    ha='right', va='bottom',
    bbox=dict(facecolor='white', alpha=0.7)
)
plt.savefig(os.path.join(GRAPH_DIR, "tempo_vs_trialname.png"))
plt.close()

# Gráfico Tamanho
plt.figure()
plt.errorbar(grouped["Query_Level"], grouped["Size_Mean"], yerr=grouped["Size_Std"], fmt='-o', color='green')
plt.xticks(grouped["Query_Level"])
plt.xlabel("Nível Lógico da Query (Trial_Name)")
plt.ylabel("Tamanho Médio da Resposta (bytes)")
plt.title("Tamanho da Resposta vs Complexidade Lógica da Query")
plt.grid(True)
plt.text(
    0.95, 0.05,
    f"ρ = {spearman_size.correlation:.3f}\np = {spearman_size.pvalue:.4f}",
    transform=plt.gca().transAxes,
    ha='right', va='bottom',
    bbox=dict(facecolor='white', alpha=0.7)
)
plt.savefig(os.path.join(GRAPH_DIR, "tamanho_vs_trialname.png"))
plt.close()

print("✅ Gráficos gerados com eixo Trial_Name (1 a 10) em 'Graficos_Incremental'")