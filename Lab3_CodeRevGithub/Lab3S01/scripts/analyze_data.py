import os
import sys
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from utils import calculate_correlation, interpret_correlation, check_correlation_significance, converter_csv_json
import base64
from io import BytesIO
import shutil
from datetime import datetime

start_time = datetime.now()
print(f"🕒 Início da execução: {start_time.strftime('%d/%m/%Y %H:%M:%S')}\n")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from config_token import configurar_token
from config_token_rotator import TokenRotator

tokens = configurar_token()
rotator = TokenRotator(tokens)

BASE_DIR = os.path.join("Lab3_CodeRevGithub", "Lab3S01")
DATA_DIR = os.path.join(BASE_DIR, "data")

def format_seconds(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

def mover_pycache(destino="Lab3_CodeRevGithub/Lab3S01/__pycache__"):
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            origem = os.path.join(root, "__pycache__")
            if os.path.abspath(origem) == os.path.abspath(destino):
                continue  # already in the right place
            os.makedirs(destino, exist_ok=True)
            for arquivo in os.listdir(origem):
                arquivo_destino = os.path.join(destino, arquivo)
                if os.path.exists(arquivo_destino):
                    os.remove(arquivo_destino)
                shutil.move(os.path.join(origem, arquivo), destino)
            shutil.rmtree(origem)
            print(f"📦 Pycache movido para: {destino}")

    sns.set(style="whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 12

def load_data(file_path):
    """
    Carrega os dados dos PRs a partir de um arquivo CSV.
    
    Args:
        file_path (str): Caminho para o arquivo CSV com os dados dos PRs
    
    Returns:
        pd.DataFrame: DataFrame com os dados dos PRs
    """
    df = pd.read_csv(file_path, sep=';')

    # Calcula o tamanho da descrição (em número de caracteres)
    df["body_length"] = df["body"].fillna("").apply(len)

    # Limpa e prepara os dados
    df.dropna(subset=["closed_at"], inplace=True)

    # Adiciona coluna com status final (MERGED ou CLOSED)
    df["status"] = df["merged"].apply(lambda x: "MERGED" if x else "CLOSED")

    # Converte datas para datetime
    for col in ["created_at", "closed_at", "merged_at"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    
    return df


def save_figure_to_file(fig, filename, dpi=300):
    """
    Salva uma figura em um arquivo.
    
    Args:
        fig (matplotlib.figure.Figure): Figura a ser salva
        filename (str): Nome do arquivo
        dpi (int): Resolução da imagem
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fig.savefig(filename, dpi=dpi, bbox_inches='tight')
    print(f"📁 Figura salva em {os.path.relpath(filename)}")
    plt.close(fig)

def figure_to_base64(fig):
    """
    Converte uma figura matplotlib para base64 para inclusão em markdown.
    
    Args:
        fig (matplotlib.figure.Figure): Figura a ser convertida
    
    Returns:
        str: String base64 da imagem
    """
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')


def create_correlation_heatmap(df, features, target, title):
    """
    Cria um mapa de calor de correlação entre várias características e um alvo.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        features (list): Lista de colunas das características
        target (str): Coluna alvo
        title (str): Título do gráfico
    
    Returns:
        matplotlib.figure.Figure: Figura com o mapa de calor
    """
    corr_data = []
    for feature in features:
        corr_val, p_val = calculate_correlation(df, feature, target, method='spearman')
        significance = '**' if check_correlation_significance(p_val) else ''
        corr_data.append({
            'Feature': feature,
            'Correlation': corr_val,
            'P-value': p_val,
            'Significance': significance
        })
    corr_df = pd.DataFrame(corr_data)
    
    fig, ax = plt.subplots(figsize=(12, len(features) * 0.8 + 2))
    bars = ax.barh(corr_df['Feature'], corr_df['Correlation'],
                    color=corr_df['Correlation'].apply(lambda x: 'skyblue' if x >= 0 else 'salmon'))
    
    for i, bar in enumerate(bars):
        significance = corr_df.iloc[i]['Significance']
        value = corr_df.iloc[i]['Correlation']
        p_value = corr_df.iloc[i]['P-value']
        if value >= 0:
            ax.text(max(value + 0.03, 0.03), i, f'{value:.3f}{significance}\np={p_value:.3e}', va='center')
        else:
            ax.text(min(value - 0.03, -0.03), i, f'{value:.3f}{significance}\np={p_value:.3e}', va='center', ha='right')
    
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    ax.set_xlim(-1, 1)
    ax.set_xlabel('Coeficiente de correlação de Spearman')
    ax.set_title(title)
    fig.text(0.9, 0.1, '** p < 0.05', fontsize=10)
    plt.tight_layout()
    return fig


def create_boxplot(df, x_col, y_col, title, xlabel, ylabel):
    """
    Cria um boxplot para comparar a distribuição de uma variável entre dois grupos.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        x_col (str): Coluna para o eixo x (categorias)
        y_col (str): Coluna para o eixo y (valores)
        title (str): Título do gráfico
        xlabel (str): Rótulo do eixo x
        ylabel (str): Rótulo do eixo y
    
    Returns:
        matplotlib.figure.Figure: Figura com o boxplot
    """
    fig, ax = plt.subplots()
    sns.boxplot(x=x_col, y=y_col, data=df, ax=ax, palette="Set2", hue=x_col, legend=False)
    sns.stripplot(x=x_col, y=y_col, data=df, ax=ax, size=4, alpha=0.3, jitter=True, color='black')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    grouped = df.groupby(x_col)[y_col]
    medians = grouped.median()
    for i, (key, median) in enumerate(medians.items()):
        ax.text(i, median * 1.1, f'Mediana: {median:.2f}', ha='center')
    
    groups = [df[df[x_col] == category][y_col].dropna() for category in df[x_col].unique()]
    if len(groups) == 2 and len(groups[0]) > 0 and len(groups[1]) > 0:
        stat, pval = stats.mannwhitneyu(groups[0], groups[1])
        ax.text(0.5, 0.01, f'Teste Mann-Whitney: p={pval:.3e}',
                ha='center', va='bottom', transform=ax.transAxes, fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8))
    plt.tight_layout()
    return fig


def create_scatter_plot(df, x_col, y_col, title, xlabel, ylabel, hue=None, log_scale=False):
    """
    Cria um gráfico de dispersão entre duas variáveis.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        x_col (str): Coluna para o eixo x
        y_col (str): Coluna para o eixo y
        title (str): Título do gráfico
        xlabel (str): Rótulo do eixo x
        ylabel (str): Rótulo do eixo y
        hue (str, optional): Coluna para colorir os pontos
        log_scale (bool, optional): Se True, aplicar escala logarítmica aos eixos
    
    Returns:
        matplotlib.figure.Figure: Figura com o gráfico de dispersão
    """
    fig, ax = plt.subplots()
    x_data = df[x_col].copy()
    y_data = df[y_col].copy()
    if x_data.dtype in [np.float64, np.int64] and y_data.dtype in [np.float64, np.int64]:
        x_quantile = np.nanquantile(x_data, 0.99)
        y_quantile = np.nanquantile(y_data, 0.99)
        filtered_df = df[(df[x_col] <= x_quantile) & (df[y_col] <= y_quantile)].copy()
    else:
        filtered_df = df.copy()
    
    if hue:
        sns.scatterplot(x=x_col, y=y_col, data=filtered_df, hue=hue, alpha=0.6, ax=ax)
        plt.legend(title=hue, loc='upper right')
    else:
        sns.scatterplot(x=x_col, y=y_col, data=filtered_df, alpha=0.6, ax=ax)
    
    if log_scale:
        if all(filtered_df[x_col] > 0):
            ax.set_xscale('log')
        if all(filtered_df[y_col] > 0):
            ax.set_yscale('log')
    
    if filtered_df[x_col].dtype in [np.float64, np.int64] and filtered_df[y_col].dtype in [np.float64, np.int64]:
        try:
            x = filtered_df[x_col].values.reshape(-1, 1)
            y = filtered_df[y_col].values
            mask = ~(np.isnan(x.flatten()) | np.isnan(y))
            x = x[mask]
            y = y[mask]
            if len(x) > 1:
                try:
                    from sklearn.linear_model import LinearRegression
                    model = LinearRegression()
                    model.fit(x, y)
                    x_range = np.linspace(min(x), max(x), 100).reshape(-1, 1)
                    y_pred = model.predict(x_range)
                    ax.plot(x_range, y_pred, color='red', linestyle='--')
                    corr_val, p_val = calculate_correlation(filtered_df, x_col, y_col, method='spearman')
                    ax.text(0.05, 0.95, f'Corr. Spearman: {corr_val:.3f}\\np-valor: {p_val:.3e}',
                            transform=ax.transAxes, fontsize=10, va='top',
                            bbox=dict(facecolor='white', alpha=0.8))
                except ImportError:
                    print("Aviso: scikit-learn não instalado; linha de tendência não adicionada.")
        except Exception as e:
            print(f"Erro ao adicionar linha de tendência: {e}")
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    return fig


def analyze_size_vs_status(df):
    results = {}
    file_status_corr, file_status_pval = calculate_correlation(df, "files_changed", "merged", method='spearman')
    adds_status_corr, adds_status_pval = calculate_correlation(df, "additions", "merged", method='spearman')
    dels_status_corr, dels_status_pval = calculate_correlation(df, "deletions", "merged", method='spearman')
    
    results["files_vs_status"] = {
        "correlation": file_status_corr,
        "p_value": file_status_pval,
        "interpretation": interpret_correlation(file_status_corr),
        "significant": check_correlation_significance(file_status_pval)
    }
    results["additions_vs_status"] = {
        "correlation": adds_status_corr,
        "p_value": adds_status_pval,
        "interpretation": interpret_correlation(adds_status_corr),
        "significant": check_correlation_significance(adds_status_pval)
    }
    results["deletions_vs_status"] = {
        "correlation": dels_status_corr,
        "p_value": dels_status_pval,
        "interpretation": interpret_correlation(dels_status_corr),
        "significant": check_correlation_significance(dels_status_pval)
    }
    
    median_stats = df.groupby("status")[["time_to_close_hours"]].median()
    median_stats["formatted"] = median_stats["time_to_close_hours"].apply(lambda h: format_seconds(h * 3600))
    results["median_stats"] = median_stats

    
    corr_fig = create_correlation_heatmap(df, ["files_changed", "additions", "deletions"], "merged",
                                        "Correlação entre Tamanho dos PRs e Status")
    results["correlation_plot"] = figure_to_base64(corr_fig)
    save_figure_to_file(corr_fig, os.path.join(DATA_DIR, "visualizations", "rq01_correlation.png"))

    
    for col, label in [("files_changed", "Número de Arquivos"),
                        ("additions", "Linhas Adicionadas"),
                        ("deletions", "Linhas Removidas")]:
        fig = create_boxplot(df, "status", col,
                            f"Distribuição de {label} por Status",
                            "Status do PR", label)
        results[f"{col}_boxplot"] = figure_to_base64(fig)
        save_figure_to_file(fig, os.path.join(DATA_DIR, "visualizations", f"rq01_{col}_boxplot.png"))
    
    return results


def analyze_time_vs_status(df):
    results = {}
    time_status_corr, time_status_pval = calculate_correlation(df, "time_to_close_hours", "merged", method='spearman')
    results["time_vs_status"] = {
        "correlation": time_status_corr,
        "p_value": time_status_pval,
        "interpretation": interpret_correlation(time_status_corr),
        "significant": check_correlation_significance(time_status_pval)
    }
    median_stats = df.groupby("status")[["time_to_close_hours"]].median()
    results["median_stats"] = median_stats
    
    fig = create_boxplot(df, "status", "time_to_close_hours",
                        "Distribuição do Tempo de Análise por Status",
                        "Status do PR", "Tempo de Análise (horas)")
    results["time_boxplot"] = figure_to_base64(fig)
    save_figure_to_file(fig, os.path.join(DATA_DIR, "visualizations", "rq02_time_boxplot.png"))
    
    fig, ax = plt.subplots()
    for status, color in zip(["MERGED", "CLOSED"], ["green", "red"]):
        subset = df[df["status"] == status]["time_to_close_hours"].dropna()
        cutoff = np.percentile(subset, 95)
        sns.histplot(subset[subset <= cutoff], ax=ax, color=color, alpha=0.5, label=status, kde=True)
    ax.set_title("Distribuição do Tempo de Análise por Status")
    ax.set_xlabel("Tempo de Análise (horas)")
    ax.set_ylabel("Contagem")
    ax.legend()
    results["time_histogram"] = figure_to_base64(fig)
    save_figure_to_file(fig, os.path.join(DATA_DIR, "visualizations", "rq02_time_histogram.png"))
    return results



def analyze_description_vs_status(df):
    results = {}
    desc_status_corr, desc_status_pval = calculate_correlation(df, "body_length", "merged", method='spearman')
    results["description_vs_status"] = {
        "correlation": desc_status_corr,
        "p_value": desc_status_pval,
        "interpretation": interpret_correlation(desc_status_corr),
        "significant": check_correlation_significance(desc_status_pval)
    }
    median_stats = df.groupby("status")[["body_length"]].median()
    results["median_stats"] = median_stats
    
    fig = create_boxplot(df, "status", "body_length",
                        "Distribuição do Tamanho da Descrição por Status",
                        "Status do PR", "Tamanho da Descrição (caracteres)")
    results["description_boxplot"] = figure_to_base64(fig)
    save_figure_to_file(fig, os.path.join(DATA_DIR, "visualizations", "rq03_description_boxplot.png"))

    fig, ax = plt.subplots()
    medians = df.groupby("status")["body_length"].median()
    bars = ax.bar(medians.index, medians.values, color=["green", "red"])
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height * 1.01,
                f'{height:.1f}', ha='center', va='bottom')
    ax.set_title("Mediana do Tamanho da Descrição por Status")
    ax.set_xlabel("Status do PR")
    ax.set_ylabel("Tamanho Mediano da Descrição (caracteres)")
    results["description_bars"] = figure_to_base64(fig)
    save_figure_to_file(fig, os.path.join(DATA_DIR, "visualizations", "rq03_description_bars.png"))
    
    return results

def analyze_interactions_vs_status(df):
    results = {}
    part_status_corr, part_status_pval = calculate_correlation(df, "participant_count", "merged", method='spearman')
    comm_status_corr, comm_status_pval = calculate_correlation(df, "comments", "merged", method='spearman')
    rev_comm_status_corr, rev_comm_status_pval = calculate_correlation(df, "review_comments", "merged", method='spearman')
    
    results["participants_vs_status"] = {
        "correlation": part_status_corr,
        "p_value": part_status_pval,
        "interpretation": interpret_correlation(part_status_corr),
        "significant": check_correlation_significance(part_status_pval)
    }
    results["comments_vs_status"] = {
        "correlation": comm_status_corr,
        "p_value": comm_status_pval,
        "interpretation": interpret_correlation(comm_status_corr),
        "significant": check_correlation_significance(comm_status_pval)
    }
    results["review_comments_vs_status"] = {
        "correlation": rev_comm_status_corr,
        "p_value": rev_comm_status_pval,
        "interpretation": interpret_correlation(rev_comm_status_corr),
        "significant": check_correlation_significance(rev_comm_status_pval)
    }
    median_stats = df.groupby("status")[["participant_count", "comments", "review_comments"]].median()
    results["median_stats"] = median_stats
    
    corr_fig = create_correlation_heatmap(df, ["participant_count", "comments", "review_comments"], "merged",
                                        "Correlação entre Interações e Status")
    results["correlation_plot"] = figure_to_base64(corr_fig)
    save_figure_to_file(corr_fig, os.path.join(DATA_DIR, "visualizations", "rq04_correlation.png"))
    
    for col, label in [("participant_count", "Número de Participantes"),
                        ("comments", "Número de Comentários"),
                        ("review_comments", "Número de Comentários de Revisão")]:
        fig = create_boxplot(df, "status", col,
                            f"Distribuição de {label} por Status",
                            "Status do PR", label)
        results[f"{col}_boxplot"] = figure_to_base64(fig)
        save_figure_to_file(fig, os.path.join(DATA_DIR, "visualizations", f"rq04_{col}_boxplot.png"))
    
    return results

def analyze_size_vs_reviews(df):
    results = {}
    file_rev_corr, file_rev_pval = calculate_correlation(df, "files_changed", "review_count", method='spearman')
    adds_rev_corr, adds_rev_pval = calculate_correlation(df, "additions", "review_count", method='spearman')
    dels_rev_corr, dels_rev_pval = calculate_correlation(df, "deletions", "review_count", method='spearman')
    
    results["files_vs_reviews"] = {
        "correlation": file_rev_corr,
        "p_value": file_rev_pval,
        "interpretation": interpret_correlation(file_rev_corr),
        "significant": check_correlation_significance(file_rev_pval)
    }
    results["additions_vs_reviews"] = {
        "correlation": adds_rev_corr,
        "p_value": adds_rev_pval,
        "interpretation": interpret_correlation(adds_rev_corr),
        "significant": check_correlation_significance(adds_rev_pval)
    }
    results["deletions_vs_reviews"] = {
        "correlation": dels_rev_corr,
        "p_value": dels_rev_pval,
        "interpretation": interpret_correlation(dels_rev_corr),
        "significant": check_correlation_significance(dels_rev_pval)
    }
    
    corr_fig = create_correlation_heatmap(df, ["files_changed", "additions", "deletions"], "review_count",
                                        "Correlação entre Tamanho dos PRs e Número de Revisões")
    results["correlation_plot"] = figure_to_base64(corr_fig)
    save_figure_to_file(corr_fig, os.path.join(DATA_DIR, "visualizations", "rq05_correlation.png"))
    
    for col, label in [("files_changed", "Número de Arquivos"),
                        ("additions", "Linhas Adicionadas"),
                        ("deletions", "Linhas Removidas")]:
        fig = create_scatter_plot(df, col, "review_count",
                                f"Relação entre {label} e Número de Revisões",
                                label, "Número de Revisões", log_scale=True)
        results[f"{col}_scatter"] = figure_to_base64(fig)
        save_figure_to_file(fig, os.path.join(DATA_DIR, "visualizations", f"rq05_{col}_scatter.png"))
    
    return results


def analyze_time_vs_reviews(df):
    results = {}
    time_rev_corr, time_rev_pval = calculate_correlation(df, "time_to_close_hours", "review_count", method='spearman')
    results["time_vs_reviews"] = {
        "correlation": time_rev_corr,
        "p_value": time_rev_pval,
        "interpretation": interpret_correlation(time_rev_corr),
        "significant": check_correlation_significance(time_rev_pval)
    }
    
    fig = create_scatter_plot(df, "time_to_close_hours", "review_count",
                                "Relação entre Tempo de Análise e Número de Revisões",
                                "Tempo de Análise (horas)", "Número de Revisões", log_scale=True)
    results["time_scatter"] = figure_to_base64(fig)
    save_figure_to_file(fig, os.path.join(DATA_DIR, "visualizations", "rq06_time_scatter.png"))
    
    fig, ax = plt.subplots()
    df['time_bins'] = pd.cut(df['time_to_close_hours'],
                            bins=[0, 24, 48, 72, 168, df['time_to_close_hours'].max()],
                            labels=['0-24h', '24-48h', '48-72h', '72h-1 semana', '> 1 semana'])
    time_bin_means = df.groupby('time_bins', observed=False)['review_count'].mean().reset_index()
    time_bin_counts = df.groupby('time_bins', observed=False).size().reset_index(name='count')
    time_bin_data = pd.merge(time_bin_means, time_bin_counts, on='time_bins')
    ax.plot(time_bin_data['time_bins'], time_bin_data['review_count'], marker='o', linestyle='-')
    for i, row in time_bin_data.iterrows():
        ax.annotate(f"n={row['count']}", (i, row['review_count']),
                    textcoords="offset points", xytext=(0, 10), ha='center')
    ax.set_title("Média de Revisões por Faixa de Tempo")
    ax.set_xlabel("Tempo de Análise")
    ax.set_ylabel("Média de Revisões")
    plt.xticks(rotation=45)
    plt.tight_layout()
    results["time_bins_plot"] = figure_to_base64(fig)
    save_figure_to_file(fig, os.path.join(DATA_DIR, "visualizations", "rq06_time_bins.png"))
    
    return results


def analyze_description_vs_reviews(df):
    results = {}
    desc_rev_corr, desc_rev_pval = calculate_correlation(df, "body_length", "review_count", method='spearman')
    results["description_vs_reviews"] = {
        "correlation": desc_rev_corr,
        "p_value": desc_rev_pval,
        "interpretation": interpret_correlation(desc_rev_corr),
        "significant": check_correlation_significance(desc_rev_pval)
    }
    
    fig = create_scatter_plot(df, "body_length", "review_count",
                            "Relação entre Tamanho da Descrição e Número de Revisões",
                            "Tamanho da Descrição (caracteres)", "Número de Revisões", log_scale=True)
    results["description_scatter"] = figure_to_base64(fig)
    save_figure_to_file(fig, os.path.join(DATA_DIR, "visualizations", "rq07_description_scatter.png"))
    
    fig, ax = plt.subplots()
    last_bin = max(2001, df['body_length'].max())
    df['desc_bins'] = pd.cut(df['body_length'],
                            bins=[0, 100, 500, 1000, 2000, last_bin],
                            labels=['0-100', '100-500', '500-1000', '1000-2000', '> 2000'])
    desc_bin_means = df.groupby('desc_bins', observed=False)['review_count'].mean().reset_index()
    desc_bin_counts = df.groupby('desc_bins', observed=False).size().reset_index(name='count')
    desc_bin_data = pd.merge(desc_bin_means, desc_bin_counts, on='desc_bins')
    bars = ax.bar(desc_bin_data['desc_bins'], desc_bin_data['review_count'])
    for i, bar in enumerate(bars):
        height = bar.get_height()
        count = desc_bin_data.iloc[i]['count']
        ax.text(bar.get_x() + bar.get_width() / 2., height + 0.1, f"n={count}", ha='center', va='bottom')
    ax.set_title("Média de Revisões por Tamanho de Descrição")
    ax.set_xlabel("Tamanho da Descrição (caracteres)")
    ax.set_ylabel("Média de Revisões")
    plt.xticks(rotation=45)
    plt.tight_layout()
    results["desc_bins_plot"] = figure_to_base64(fig)
    save_figure_to_file(fig, os.path.join(DATA_DIR, "visualizations", "rq07_desc_bins.png"))
    
    return results


def analyze_interactions_vs_reviews(df):
    results = {}
    part_rev_corr, part_rev_pval = calculate_correlation(df, "participant_count", "review_count", method='spearman')
    comm_rev_corr, comm_rev_pval = calculate_correlation(df, "comments", "review_count", method='spearman')
    rev_comm_rev_corr, rev_comm_rev_pval = calculate_correlation(df, "review_comments", "review_count", method='spearman')
    
    results["participants_vs_reviews"] = {
        "correlation": part_rev_corr,
        "p_value": part_rev_pval,
        "interpretation": interpret_correlation(part_rev_corr),
        "significant": check_correlation_significance(part_rev_pval)
    }
    results["comments_vs_reviews"] = {
        "correlation": comm_rev_corr,
        "p_value": comm_rev_pval,
        "interpretation": interpret_correlation(comm_rev_corr),
        "significant": check_correlation_significance(comm_rev_pval)
    }
    results["review_comments_vs_reviews"] = {
        "correlation": rev_comm_rev_corr,
        "p_value": rev_comm_rev_pval,
        "interpretation": interpret_correlation(rev_comm_rev_corr),
        "significant": check_correlation_significance(rev_comm_rev_pval)
    }
    
    corr_fig = create_correlation_heatmap(df, ["participant_count", "comments", "review_comments"],
                                        "review_count", "Correlação entre Interações e Número de Revisões")
    results["correlation_plot"] = figure_to_base64(corr_fig)
    save_figure_to_file(corr_fig, os.path.join(DATA_DIR, "visualizations", "rq08_correlation.png"))
    
    for col, label in [("participant_count", "Número de Participantes"),
                        ("comments", "Número de Comentários"),
                        ("review_comments", "Número de Comentários de Revisão")]:
        fig = create_scatter_plot(df, col, "review_count",
                                f"Relação entre {label} e Número de Revisões",
                                label, "Número de Revisões")
        results[f"{col}_scatter"] = figure_to_base64(fig)
        save_figure_to_file(fig, os.path.join(DATA_DIR, "visualizations", f"rq08_{col}_scatter.png"))

    
    return results


def generate_report(all_results, output_file="report.md"):
    os.makedirs("data/visualizations", exist_ok=True)
    report = []

    # Título
    report.append("\n#📄 **Relatório de Análise da Atividade de Code Review no GitHub**\n")

    # Introdução
    report.append("\n## 📋 **Introdução**\n")
    report.append("Este relatório apresenta os resultados da análise da atividade de code review em repositórios populares do GitHub. O objetivo é identificar variáveis que influenciam no merge de um PR, sob a perspectiva de desenvolvedores que submetem código aos repositórios selecionados.\n")

    report.append("\n### ✨ **Hipóteses Informais**\n")
    report.append("1. PRs menores têm maior probabilidade de serem aprovados. ✂️\n")
    report.append("2. PRs que levam mais tempo para serem analisados têm menor probabilidade de serem aprovados. ⏳❌\n")
    report.append("3. PRs com descrições mais detalhadas têm maior probabilidade de serem aprovados. 📑👍\n")
    report.append("4. PRs com mais interações têm maior probabilidade de serem aprovados. 💬🔄\n")
    report.append("5. PRs maiores requerem mais revisões. 📂🔍\n")
    report.append("6. PRs que levam mais tempo para serem analisados têm mais revisões. ⏱️🔄\n")
    report.append("7. PRs com descrições mais detalhadas têm menos revisões. ✍️📉\n")
    report.append("8. PRs com mais interações têm mais revisões. 💬🔄✅\n")

    # Metodologia
    report.append("\n## 🧑‍🔬 **Metodologia**\n")
    report.append("1. Coleta de dados: Selecionamos os 200 repositórios mais populares do GitHub com pelo menos 100 PRs (MERGED + CLOSED).\n")
    report.append("2. Filtragem dos dados: Selecionamos apenas PRs com status MERGED ou CLOSED, que possuíam pelo menos uma revisão e cuja análise levou pelo menos uma hora.\n")
    report.append("3. Análise estatística: Utilizamos o coeficiente de correlação de Spearman para analisar as relações entre as variáveis.\n")
    report.append("4. Interpretação dos resultados: Interpretamos os coeficientes de correlação conforme faixas de força e p-valores.\n")

    # Resultados
    report.append("\n## 📊 **Resultados**\n")

    report.append("\n### RQ 01: Relação entre o tamanho dos PRs e o feedback final das revisões\n")
    if "size_vs_status" in all_results:
        results = all_results["size_vs_status"]
        report.append("**📏 Correlação entre métricas de tamanho e status:**\n")
        report.append("![Correlação entre Tamanho dos PRs e Status](./visualizations/rq01_correlation.png)\n")
        report.append("**📂 Correlação entre número de arquivos alterados e status:**\n")
        report.append(f"- Coeficiente de correlação: {results['files_vs_status']['correlation']:.4f}\n")
        report.append(f"- P-valor: {results['files_vs_status']['p_value']:.4e}\n")
        report.append(f"- Interpretação: {results['files_vs_status']['interpretation']}\n")
        report.append(f"- Estatisticamente significativo: {'✅ Sim' if results['files_vs_status']['significant'] else '❌ Não'}\n")
        report.append("![Distribuição de Arquivos por Status](./visualizations/rq01_files_changed_boxplot.png)\n")

    report.append("\n### RQ 02: Relação entre o tempo de análise dos PRs e o feedback final das revisões\n")
    if "time_vs_status" in all_results:
        results = all_results["time_vs_status"]
        report.append("**⏱️ Correlação entre tempo de análise e status:**\n")
        report.append(f"- Coeficiente de correlação: {results['time_vs_status']['correlation']:.4f}\n")
        report.append(f"- P-valor: {results['time_vs_status']['p_value']:.4e}\n")
        report.append(f"- Interpretação: {results['time_vs_status']['interpretation']}\n")
        report.append(f"- Estatisticamente significativo: {'✅ Sim' if results['time_vs_status']['significant'] else '❌ Não'}\n")
        report.append("![Distribuição do Tempo de Análise por Status](./visualizations/rq02_time_boxplot.png)\n")
        report.append("![Histograma do Tempo de Análise por Status](./visualizations/rq02_time_histogram.png)\n")

    # Conclusão
    report.append("\n## 🔍 **Conclusão**\n")
    report.append("Este estudo analisou a relação entre diversas características dos PRs e seu feedback final, bem como o número de revisões realizadas.\n")
    report.append("Com base nos resultados, podemos sugerir boas práticas para submissão de PRs mais eficazes.\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print(f"📄 Relatório gerado com sucesso em {output_file}")

def main():
    converter_csv_json()

    os.makedirs(DATA_DIR, exist_ok=True)
    visual_dir = os.path.join(DATA_DIR, "visualizations")
    os.makedirs(visual_dir, exist_ok=True)

    csv_path = os.path.join(DATA_DIR, "collected_prs.csv")
    report_path = os.path.join(DATA_DIR, f"report.md")

    print("\n📂 Arquivos de Dados e Relatórios")
    print(f"   📊 Arquivo de dados dos PRs a ser analisado: {csv_path}")
    print(f"   📈 Relatório final será salvo em: {report_path}")
    print(f"   📊 Visualizações serão salvas em: {visual_dir}")

    print("\n📂 Diretórios de Salvamento")
    print(f"   📍 Os dados serão salvos no diretório: {DATA_DIR}")
    print(f"   📍 Caminho para o arquivo de PRs coletados: {csv_path}")
    print(f"   📍 Caminho para o relatório final: {report_path}")
    print(f"   📍 Caminho para as visualizações: {visual_dir}\n")

    df = load_data(csv_path)
    print(f"📈 Dados carregados com sucesso. Total de {len(df)} PRs.\n")

    all_results = {}
    print("\n🔍 Analisando RQ 01: Tamanho vs. Status...")
    all_results["size_vs_status"] = analyze_size_vs_status(df)

    print("\n🔍 Analisando RQ 02: Tempo vs. Status...")
    all_results["time_vs_status"] = analyze_time_vs_status(df)

    print("\n🔍 Analisando RQ 03: Descrição vs. Status...")
    all_results["description_vs_status"] = analyze_description_vs_status(df)

    print("\n🔍 Analisando RQ 04: Interações vs. Status...")
    all_results["interactions_vs_status"] = analyze_interactions_vs_status(df)

    print("\n🔍 Analisando RQ 05: Tamanho vs. Revisões...")
    all_results["size_vs_reviews"] = analyze_size_vs_reviews(df)

    print("\n🔍 Analisando RQ 06: Tempo vs. Revisões...")
    all_results["time_vs_reviews"] = analyze_time_vs_reviews(df)

    print("\n🔍 Analisando RQ 07: Descrição vs. Revisões...")
    all_results["description_vs_reviews"] = analyze_description_vs_reviews(df)

    print("\n🔍 Analisando RQ 08: Interações vs. Revisões...")
    all_results["interactions_vs_reviews"] = analyze_interactions_vs_reviews(df)

    print("\n📑 Gerando relatório final...")
    generate_report(all_results, output_file=report_path)

    # Remover colunas temporárias se existirem
    if 'time_bins' in df.columns:
        df.drop(columns=['time_bins'], inplace=True)
    if 'desc_bins' in df.columns:
        df.drop(columns=['desc_bins'], inplace=True)

    print("\n📦 Resumo dos arquivos gerados:\n")
    print(f"🔹 {os.path.relpath(csv_path)}")
    print("    ↪️ Arquivo CSV contendo todos os Pull Requests analisados (dados brutos, um por linha).")

    print(f"🔹 {os.path.relpath(report_path)}")
    print("    ↪️ Relatório completo em Markdown com todas as análises, gráficos e interpretações.")

    print(f"🔹 {os.path.relpath(visual_dir)}")
    print("    ↪️ Pasta com os gráficos PNG gerados para cada pergunta de pesquisa (RQ01 a RQ08).\n")

    print(f"✅ Análise concluída com sucesso! Relatório salvo em {os.path.relpath(report_path)}")

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"\n🕔 Fim da execução: {end_time.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"⏱️ Duração total: {str(duration)}\n")

if __name__ == "__main__":
    main()
    mover_pycache()
