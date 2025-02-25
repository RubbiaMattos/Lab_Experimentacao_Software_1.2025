import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_correlations(data):
    """
    Plota gráficos de correlação.
    """
    sns.pairplot(data, kind="reg")
    plt.savefig("data/results/correlation_plots.png")

if __name__ == "__main__":
    DATA_PATH = "data/results/summary.csv"
    data = pd.read_csv(DATA_PATH)
    plot_correlations(data)