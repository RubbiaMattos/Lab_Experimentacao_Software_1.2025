import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from utils import calculate_correlation, interpret_correlation, check_correlation_significance
import base64
from io import BytesIO

# Configurar o estilo das visualizações
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
    df = pd.read_csv(file_path)

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
    # Calcular correlações
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

    # Criar figura
    fig, ax = plt.subplots(figsize=(12, len(features) * 0.8 + 2))

    # Plotar barras horizontais
    bars = ax.barh(corr_df['Feature'], corr_df['Correlation'],
                   color=corr_df['Correlation'].apply(lambda x: 'skyblue' if x >= 0 else 'salmon'))

    # Adicionar valores e significância estatística
    for i, bar in enumerate(bars):
        significance = corr_df.iloc[i]['Significance']
        value = corr_df.iloc[i]['Correlation']
        p_value = corr_df.iloc[i]['P-value']

        # Posicionar texto
        if value >= 0:
            ax.text(max(value + 0.03, 0.03), i, f'{value:.3f}{significance}\np={p_value:.3e}', va='center')
        else:
            ax.text(min(value - 0.03, -0.03), i, f'{value:.3f}{significance}\np={p_value:.3e}', va='center', ha='right')

    # Configurar eixos
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    ax.set_xlim(-1, 1)
    ax.set_xlabel('Coeficiente de correlação de Spearman')
    ax.set_title(title)

    # Adicionar legenda para significância
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
    # Criar figura
    fig, ax = plt.subplots()

    # Plotar boxplot
    sns.boxplot(x=x_col, y=y_col, data=df, ax=ax, palette="Set2")

    # Adicionar pontos individuais para visualizar a distribuição
    sns.stripplot(x=x_col, y=y_col, data=df, ax=ax, size=4, alpha=0.3, jitter=True, color='black')

    # Configurar rótulos
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Adicionar estatísticas
    grouped = df.groupby(x_col)[y_col]
    medians = grouped.median()

    for i, (key, median) in enumerate(medians.items()):
        ax.text(i, median * 1.1, f'Mediana: {median:.2f}', ha='center')

    # Realizar teste estatístico
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
    # Criar figura
    fig, ax = plt.subplots()

    # Filtar outliers extremos para melhor visualização (mantendo 99% dos dados)
    x_data = df[x_col].copy()
    y_data = df[y_col].copy()

    if x_data.dtype in [np.float64, np.int64] and y_data.dtype in [np.float64, np.int64]:
        x_quantile = np.nanquantile(x_data, 0.99)
        y_quantile = np.nanquantile(y_data, 0.99)

        filtered_df = df[(df[x_col] <= x_quantile) & (df[y_col] <= y_quantile)].copy()
    else:
        filtered_df = df.copy()

    # Plotar gráfico de dispersão
    if hue:
        scatter = sns.scatterplot(x=x_col, y=y_col, data=filtered_df, hue=hue, alpha=0.6, ax=ax)
        plt.legend(title=hue, loc='upper right')
    else:
        scatter = sns.scatterplot(x=x_col, y=y_col, data=filtered_df, alpha=0.6, ax=ax)

    # Aplicar escala logarítmica se necessário
    if log_scale:
        if all(filtered_df[x_col] > 0):
            ax.set_xscale('log')
        if all(filtered_df[y_col] > 0):
            ax.set_yscale('log')

    # Adicionar linha de tendência
    if filtered_df[x_col].dtype in [np.float64, np.int64] and filtered_df[y_col].dtype in [np.float64, np.int64]:
        try:
            x = filtered_df[x_col].values.reshape(-1, 1)
            y = filtered_df[y_col].values

            # Remover NaNs
            mask = ~(np.isnan(x.flatten()) | np.isnan(y))
            x = x[mask]
            y = y[mask]

            if len(x) > 1:  # Verificar se há dados suficientes
                from sklearn.linear_model import LinearRegression
                model = LinearRegression()
                model.fit(x, y)

                x_range = np.linspace(min(x), max(x), 100).reshape(-1, 1)
                y_pred = model.predict(x_range)

                ax.plot(x_range, y_pred, color='red', linestyle='--')

                # Adicionar coeficiente de correlação
                corr_val, p_val = calculate_correlation(filtered_df, x_col, y_col, method='spearman')
                ax.text(0.05, 0.95, f'Corr. Spearman: {corr_val:.3f}\np-valor: {p_val:.3e}',
                        transform=ax.transAxes, fontsize=10, va='top',
                        bbox=dict(facecolor='white', alpha=0.8))
        except Exception as e:
            print(f"Erro ao adicionar linha de tendência: {e}")

    # Configurar rótulos
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    plt.tight_layout()
    return fig


def analyze_size_vs_status(df):
    """
    RQ 01: Analisa a relação entre o tamanho dos PRs e o feedback final das revisões.

    Args:
        df (pd.DataFrame): DataFrame com os dados dos PRs

    Returns:
        dict: Dicionário com os resultados da análise
    """
    results = {}

    # Correlação entre número de arquivos e status
    file_status_corr, file_status_pval = calculate_correlation(
        df, "files_changed", "merged", method="spearman"
    )

    # Correlação entre linhas adicionadas e status
    adds_status_corr, adds_status_pval = calculate_correlation(
        df, "additions", "merged", method="spearman"
    )

    # Correlação entre linhas removidas e status
    dels_status_corr, dels_status_pval = calculate_correlation(
        df, "deletions", "merged", method="spearman"
    )

    # Armazena os resultados
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

    # Estatísticas descritivas por status
    median_stats = df.groupby("status")[["files_changed", "additions", "deletions"]].median()
    results["median_stats"] = median_stats

    # Criar visualizações
    # 1. Mapa de calor de correlação
    corr_fig = create_correlation_heatmap(
        df,
        ["files_changed", "additions", "deletions"],
        "merged",
        "Correlação entre Tamanho dos PRs e Status"
    )
    results["correlation_plot"] = figure_to_base64(corr_fig)
    save_figure_to_file(corr_fig, "data/visualizations/rq01_correlation.png")

    # 2. Boxplots comparando distribuições
    for col, label in [
        ("files_changed", "Número de Arquivos"),
        ("additions", "Linhas Adicionadas"),
        ("deletions", "Linhas Removidas")
    ]:
        fig = create_boxplot(
            df,
            "status",
            col,
            f"Distribuição de {label} por Status",
            "Status do PR",
            label
        )
        results[f"{col}_boxplot"] = figure_to_base64(fig)
        save_figure_to_file(fig, f"data/visualizations/rq01_{col}_boxplot.png")

    return results


def analyze_time_vs_status(df):
    """
    RQ 02: Analisa a relação entre o tempo de análise dos PRs e o feedback final das revisões.

    Args:
        df (pd.DataFrame): DataFrame com os dados dos PRs

    Returns:
        dict: Dicionário com os resultados da análise
    """
    results = {}

    # Correlação entre tempo para fechar e status
    time_status_corr, time_status_pval = calculate_correlation(
        df, "time_to_close_hours", "merged", method="spearman"
    )

    # Armazena os resultados
    results["time_vs_status"] = {
        "correlation": time_status_corr,
        "p_value": time_status_pval,
        "interpretation": interpret_correlation(time_status_corr),
        "significant": check_correlation_significance(time_status_pval)
    }

    # Estatísticas descritivas por status
    median_stats = df.groupby("status")[["time_to_close_hours"]].median()
    results["median_stats"] = median_stats

    # Criar visualizações
    # 1. Boxplot comparando distribuições
    fig = create_boxplot(
        df,
        "status",
        "time_to_close_hours",
        "Distribuição do Tempo de Análise por Status",
        "Status do PR",
        "Tempo de Análise (horas)"
    )
    results["time_boxplot"] = figure_to_base64(fig)
    save_figure_to_file(fig, "data/visualizations/rq02_time_boxplot.png")

    # 2. Histograma comparando distribuições
    fig, ax = plt.subplots()
    for status, color in zip(["MERGED", "CLOSED"], ["green", "red"]):
        subset = df[df["status"] == status]["time_to_close_hours"].dropna()
        # Limitar a 95% dos dados para melhor visualização
        cutoff = np.percentile(subset, 95)
        sns.histplot(subset[subset <= cutoff], ax=ax, color=color, alpha=0.5, label=status, kde=True)

    ax.set_title("Distribuição do Tempo de Análise por Status")
    ax.set_xlabel("Tempo de Análise (horas)")
    ax.set_ylabel("Contagem")
    ax.legend()

    results["time_histogram"] = figure_to_base64(fig)
    save_figure_to_file(fig, "data/visualizations/rq02_time_histogram.png")

    return results


def analyze_description_vs_status(df):
    """
    RQ 03: Analisa a relação entre a descrição dos PRs e o feedback final das revisões.

    Args:
        df (pd.DataFrame): DataFrame com os dados dos PRs

    Returns:
        dict: Dicionário com os resultados da análise
    """
    results = {}

    # Correlação entre tamanho da descrição e status
    desc_status_corr, desc_status_pval = calculate_correlation(
        df, "body_length", "merged", method="spearman"
    )

    # Armazena os resultados
    results["description_vs_status"] = {
        "correlation": desc_status_corr,
        "p_value": desc_status_pval,
        "interpretation": interpret_correlation(desc_status_corr),
        "significant": check_correlation_significance(desc_status_pval)
    }

    # Estatísticas descritivas por status
    median_stats = df.groupby("status")[["body_length"]].median()
    results["median_stats"] = median_stats

    # Criar visualizações
    # 1. Boxplot comparando distribuições
    fig = create_boxplot(
        df,
        "status",
        "body_length",
        "Distribuição do Tamanho da Descrição por Status",
        "Status do PR",
        "Tamanho da Descrição (caracteres)"
    )
    results["description_boxplot"] = figure_to_base64(fig)
    save_figure_to_file(fig, "data/visualizations/rq03_description_boxplot.png")

    # 2. Gráfico de barras com medianas
    fig, ax = plt.subplots()
    medians = df.groupby("status")["body_length"].median()
    bars = ax.bar(medians.index, medians.values, color=["green", "red"])

    # Adicionar valores
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height * 1.01,
                f'{height:.1f}', ha='center', va='bottom')

    ax.set_title("Mediana do Tamanho da Descrição por Status")
    ax.set_xlabel("Status do PR")
    ax.set_ylabel("Tamanho Mediano da Descrição (caracteres)")

    results["description_bars"] = figure_to_base64(fig)
    save_figure_to_file(fig, "data/visualizations/rq03_description_bars.png")

    return results


def analyze_interactions_vs_status(df):
    """
    RQ 04: Analisa a relação entre as interações nos PRs e o feedback final das revisões.

    Args:
        df (pd.DataFrame): DataFrame com os dados dos PRs

    Returns:
        dict: Dicionário com os resultados da análise
    """
    results = {}

    # Correlação entre número de participantes e status
    part_status_corr, part_status_pval = calculate_correlation(
        df, "participant_count", "merged", method="spearman"
    )

    # Correlação entre número de comentários e status
    comm_status_corr, comm_status_pval = calculate_correlation(
        df, "comments", "merged", method="spearman"
    )

    # Correlação entre número de comentários de revisão e status
    rev_comm_status_corr, rev_comm_status_pval = calculate_correlation(
        df, "review_comments", "merged", method="spearman"
    )

    # Armazena os resultados
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

    # Estatísticas descritivas por status
    median_stats = df.groupby("status")[["participant_count", "comments", "review_comments"]].median()
    results["median_stats"] = median_stats

    # Criar visualizações
    # 1. Mapa de calor de correlação
    corr_fig = create_correlation_heatmap(
        df,
        ["participant_count", "comments", "review_comments"],
        "merged",
        "Correlação entre Interações e Status"
    )
    results["correlation_plot"] = figure_to_base64(corr_fig)
    save_figure_to_file(corr_fig, "data/visualizations/rq04_correlation.png")

    # 2. Boxplots comparando distribuições
    for col, label in [
        ("participant_count", "Número de Participantes"),
        ("comments", "Número de Comentários"),
        ("review_comments", "Número de Comentários de Revisão")
    ]:
        fig = create_boxplot(
            df,
            "status",
            col,
            f"Distribuição de {label} por Status",
            "Status do PR",
            label
        )
        results[f"{col}_boxplot"] = figure_to_base64(fig)
        save_figure_to_file(fig, f"data/visualizations/rq04_{col}_boxplot.png")

    return results


def analyze_size_vs_reviews(df):
    """
    RQ 05: Analisa a relação entre o tamanho dos PRs e o número de revisões realizadas.

    Args:
        df (pd.DataFrame): DataFrame com os dados dos PRs

    Returns:
        dict: Dicionário com os resultados da análise
    """
    results = {}

    # Correlação entre número de arquivos e número de revisões
    file_rev_corr, file_rev_pval = calculate_correlation(
        df, "files_changed", "review_count", method="spearman"
    )

    # Correlação entre linhas adicionadas e número de revisões
    adds_rev_corr, adds_rev_pval = calculate_correlation(
        df, "additions", "review_count", method="spearman"
    )

    # Correlação entre linhas removidas e número de revisões
    dels_rev_corr, dels_rev_pval = calculate_correlation(
        df, "deletions", "review_count", method="spearman"
    )

    # Armazena os resultados
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

    # Criar visualizações
    # 1. Mapa de calor de correlação
    corr_fig = create_correlation_heatmap(
        df,
        ["files_changed", "additions", "deletions"],
        "review_count",
        "Correlação entre Tamanho dos PRs e Número de Revisões"
    )
    results["correlation_plot"] = figure_to_base64(corr_fig)
    save_figure_to_file(corr_fig, "data/visualizations/rq05_correlation.png")

    # 2. Scatter plots
    for col, label in [
        ("files_changed", "Número de Arquivos"),
        ("additions", "Linhas Adicionadas"),
        ("deletions", "Linhas Removidas")
    ]:
        fig = create_scatter_plot(
            df,
            col,
            "review_count",
            f"Relação entre {label} e Número de Revisões",
            label,
            "Número de Revisões",
            log_scale=True
        )
        results[f"{col}_scatter"] = figure_to_base64(fig)
        save_figure_to_file(fig, f"data/visualizations/rq05_{col}_scatter.png")

    return results


def analyze_time_vs_reviews(df):
    """
    RQ 06: Analisa a relação entre o tempo de análise dos PRs e o número de revisões realizadas.

    Args:
        df (pd.DataFrame): DataFrame com os dados dos PRs

    Returns:
        dict: Dicionário com os resultados da análise
    """
    results = {}

    # Correlação entre tempo para fechar e número de revisões
    time_rev_corr, time_rev_pval = calculate_correlation(
        df, "time_to_close_hours", "review_count", method="spearman"
    )

    # Armazena os resultados
    results["time_vs_reviews"] = {
        "correlation": time_rev_corr,
        "p_value": time_rev_pval,
        "interpretation": interpret_correlation(time_rev_corr),
        "significant": check_correlation_significance(time_rev_pval)
    }

    # Criar visualizações
    # 1. Scatter plot
    fig = create_scatter_plot(
        df,
        "time_to_close_hours",
        "review_count",
        "Relação entre Tempo de Análise e Número de Revisões",
        "Tempo de Análise (horas)",
        "Número de Revisões",
        log_scale=True
    )
    results["time_scatter"] = figure_to_base64(fig)
    save_figure_to_file(fig, "data/visualizations/rq06_time_scatter.png")

    # 2. Gráfico de linha para média de revisões por faixas de tempo
    fig, ax = plt.subplots()

    # Criar bins para o tempo
    df['time_bins'] = pd.cut(df['time_to_close_hours'],
                             bins=[0, 24, 48, 72, 168, df['time_to_close_hours'].max()],
                             labels=['0-24h', '24-48h', '48-72h', '72h-1 semana', '> 1 semana'])

    # Calcular média de revisões por bin
    time_bin_means = df.groupby('time_bins')['review_count'].mean().reset_index()
    time_bin_counts = df.groupby('time_bins').size().reset_index(name='count')
    time_bin_data = pd.merge(time_bin_means, time_bin_counts, on='time_bins')

    # Plotar gráfico de linhas
    ax.plot(time_bin_data['time_bins'], time_bin_data['review_count'], marker='o', linestyle='-')

    # Adicionar contagem em cada ponto
    for i, row in time_bin_data.iterrows():
        ax.annotate(f"n={row['count']}",
                    (i, row['review_count']),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center')

    ax.set_title("Média de Revisões por Faixa de Tempo")
    ax.set_xlabel("Tempo de Análise")
    ax.set_ylabel("Média de Revisões")
    plt.xticks(rotation=45)
    plt.tight_layout()

    results["time_bins_plot"] = figure_to_base64(fig)
    save_figure_to_file(fig, "data/visualizations/rq06_time_bins.png")

    return results


def analyze_description_vs_reviews(df):
    """
    RQ 07: Analisa a relação entre a descrição dos PRs e o número de revisões realizadas.

    Args:
        df (pd.DataFrame): DataFrame com os dados dos PRs

    Returns:
        dict: Dicionário com os resultados da análise
    """
    results = {}

    # Correlação entre tamanho da descrição e número de revisões
    desc_rev_corr, desc_rev_pval = calculate_correlation(
        df, "body_length", "review_count", method="spearman"
    )

    # Armazena os resultados
    results["description_vs_reviews"] = {
        "correlation": desc_rev_corr,
        "p_value": desc_rev_pval,
        "interpretation": interpret_correlation(desc_rev_corr),
        "significant": check_correlation_significance(desc_rev_pval)
    }

    # Criar visualizações
    # 1. Scatter plot
    fig = create_scatter_plot(
        df,
        "body_length",
        "review_count",
        "Relação entre Tamanho da Descrição e Número de Revisões",
        "Tamanho da Descrição (caracteres)",
        "Número de Revisões",
        log_scale=True
    )
    results["description_scatter"] = figure_to_base64(fig)
    save_figure_to_file(fig, "data/visualizations/rq07_description_scatter.png")

    # 2. Gráfico de barras para média de revisões por faixas de tamanho de descrição
    fig, ax = plt.subplots()

    # Criar bins para o tamanho da descrição
    df['desc_bins'] = pd.cut(df['body_length'],
                             bins=[0, 100, 500, 1000, 2000, df['body_length'].max()],
                             labels=['0-100', '100-500', '500-1000', '1000-2000', '> 2000'])

    # Calcular média de revisões por bin
    desc_bin_means = df.groupby('desc_bins')['review_count'].mean().reset_index()
    desc_bin_counts = df.groupby('desc_bins').size().reset_index(name='count')
    desc_bin_data = pd.merge(desc_bin_means, desc_bin_counts, on='desc_bins')

    # Plotar gráfico de barras
    bars = ax.bar(desc_bin_data['desc_bins'], desc_bin_data['review_count'])

    # Adicionar contagem em cada barra
    for i, bar in enumerate(bars):
        height = bar.get_height()
        count = desc_bin_data.iloc[i]['count']
        ax.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                f"n={count}", ha='center', va='bottom')

    ax.set_title("Média de Revisões por Tamanho de Descrição")
    ax.set_xlabel("Tamanho da Descrição (caracteres)")
    ax.set_ylabel("Média de Revisões")
    plt.xticks(rotation=45)
    plt.tight_layout()

    results["desc_bins_plot"] = figure_to_base64(fig)
    save_figure_to_file(fig, "data/visualizations/rq07_desc_bins.png")

    return results


def analyze_interactions_vs_reviews(df):
    """
    RQ 08: Analisa a relação entre as interações nos PRs e o número de revisões realizadas.

    Args:
        df (pd.DataFrame): DataFrame com os dados dos PRs

    Returns:
        dict: Dicionário com os resultados da análise
    """
    results = {}

    # Correlação entre número de participantes e número de revisões
    part_rev_corr, part_rev_pval = calculate_correlation(
        df, "participant_count", "review_count", method="spearman"
    )

    # Correlação entre número de comentários e número de revisões
    comm_rev_corr, comm_rev_pval = calculate_correlation(
        df, "comments", "review_count", method="spearman"
    )

    # Correlação entre número de comentários de revisão e número de revisões
    rev_comm_rev_corr, rev_comm_rev_pval = calculate_correlation(
        df, "review_comments", "review_count", method="spearman"
    )

    # Armazena os resultados
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

    # Criar visualizações
    # 1. Mapa de calor de correlação
    corr_fig = create_correlation_heatmap(
        df,
        ["participant_count", "comments", "review_comments"],
        "review_count",
        "Correlação entre Interações e Número de Revisões"
    )
    results["correlation_plot"] = figure_to_base64(corr_fig)
    save_figure_to_file(corr_fig, "data/visualizations/rq08_correlation.png")

    # 2. Scatter plots
    for col, label in [
        ("participant_count", "Número de Participantes"),
        ("comments", "Número de Comentários"),
        ("review_comments", "Número de Comentários de Revisão")
    ]:
        fig = create_scatter_plot(
            df,
            col,
            "review_count",
            f"Relação entre {label} e Número de Revisões",
            label,
            "Número de Revisões"
        )
        results[f"{col}_scatter"] = figure_to_base64(fig)
        save_figure_to_file(fig, f"data/visualizations/rq08_{col}_scatter.png")

    return results


def generate_report(all_results, output_file="report.md"):
    """
    Gera um relatório com os resultados das análises.

    Args:
        all_results (dict): Dicionário com todos os resultados das análises
        output_file (str): Caminho para o arquivo de saída do relatório
    """
    # Criar diretório para visualizações se não existir
    os.makedirs("data/visualizations", exist_ok=True)

    report = []

    # Título e introdução
    report.append("# Relatório de Análise da Atividade de Code Review no GitHub")
    report.append("\n## Introdução")
    report.append(
        "\nEste relatório apresenta os resultados da análise da atividade de code review em repositórios populares do GitHub. O objetivo é identificar variáveis que influenciam no merge de um PR, sob a perspectiva de desenvolvedores que submetem código aos repositórios selecionados.")
    report.append("\n### Hipóteses Informais")
    report.append("\n1. PRs menores têm maior probabilidade de serem aprovados.")
    report.append("2. PRs que levam mais tempo para serem analisados têm menor probabilidade de serem aprovados.")
    report.append("3. PRs com descrições mais detalhadas têm maior probabilidade de serem aprovados.")
    report.append("4. PRs com mais interações têm maior probabilidade de serem aprovados.")
    report.append("5. PRs maiores requerem mais revisões.")
    report.append("6. PRs que levam mais tempo para serem analisados têm mais revisões.")
    report.append("7. PRs com descrições mais detalhadas têm menos revisões.")
    report.append("8. PRs com mais interações têm mais revisões.")

    # Metodologia
    report.append("\n## Metodologia")
    report.append("\nPara realizar esta análise, seguimos os seguintes passos:")
    report.append(
        "\n1. **Coleta de dados**: Selecionamos os 200 repositórios mais populares do GitHub com pelo menos 100 PRs (MERGED + CLOSED).")
    report.append(
        "\n2. **Filtragem dos dados**: Selecionamos apenas PRs com status MERGED ou CLOSED, que possuíam pelo menos uma revisão e cuja análise levou pelo menos uma hora.")
    report.append(
        "\n3. **Análise estatística**: Utilizamos o coeficiente de correlação de Spearman para analisar as relações entre as variáveis, pois esse método não assume que os dados seguem uma distribuição normal e é menos sensível a outliers. O coeficiente de Spearman é adequado para dados que não necessariamente têm uma relação linear, medindo a força e direção de uma associação monotônica entre duas variáveis.")
    report.append(
        "\n4. **Interpretação dos resultados**: Interpretamos os coeficientes de correlação da seguinte forma:")
    report.append("   - |r| < 0.1: Correlação insignificante")
    report.append("   - 0.1 ≤ |r| < 0.3: Correlação fraca")
    report.append("   - 0.3 ≤ |r| < 0.5: Correlação moderada")
    report.append("   - 0.5 ≤ |r| < 0.7: Correlação forte")
    report.append("   - |r| ≥ 0.7: Correlação muito forte")
    report.append("\n   Consideramos correlações estatisticamente significativas aquelas com p-valor < 0.05.")

    # Resultados
    report.append("\n## Resultados")

    # RQ 01
    report.append("\n### RQ 01: Relação entre o tamanho dos PRs e o feedback final das revisões")

    if "size_vs_status" in all_results:
        results = all_results["size_vs_status"]

        # Adicionar visualização principal
        report.append("\n**Correlação entre métricas de tamanho e status:**")
        report.append(f"\n![Correlação entre Tamanho dos PRs e Status](data/visualizations/rq01_correlation.png)")

        report.append("\n**Correlação entre número de arquivos alterados e status:**")
        report.append(f"- Coeficiente de correlação: {results['files_vs_status']['correlation']:.4f}")
        report.append(f"- P-valor: {results['files_vs_status']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['files_vs_status']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['files_vs_status']['significant'] else 'Não'}")

        # Adicionar visualização de arquivo
        report.append(f"\n![Distribuição de Arquivos por Status](data/visualizations/rq01_files_changed_boxplot.png)")

        report.append("\n**Correlação entre linhas adicionadas e status:**")
        report.append(f"- Coeficiente de correlação: {results['additions_vs_status']['correlation']:.4f}")
        report.append(f"- P-valor: {results['additions_vs_status']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['additions_vs_status']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['additions_vs_status']['significant'] else 'Não'}")

        # Adicionar visualização de adições
        report.append(
            f"\n![Distribuição de Linhas Adicionadas por Status](data/visualizations/rq01_additions_boxplot.png)")

        report.append("\n**Correlação entre linhas removidas e status:**")
        report.append(f"- Coeficiente de correlação: {results['deletions_vs_status']['correlation']:.4f}")
        report.append(f"- P-valor: {results['deletions_vs_status']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['deletions_vs_status']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['deletions_vs_status']['significant'] else 'Não'}")

        # Adicionar visualização de remoções
        report.append(
            f"\n![Distribuição de Linhas Removidas por Status](data/visualizations/rq01_deletions_boxplot.png)")

        report.append("\n**Estatísticas descritivas (medianas):**")
        report.append(f"- PRs mesclados (MERGED):")
        report.append(f"  - Arquivos alterados: {results['median_stats'].loc['MERGED', 'files_changed']:.2f}")
        report.append(f"  - Linhas adicionadas: {results['median_stats'].loc['MERGED', 'additions']:.2f}")
        report.append(f"  - Linhas removidas: {results['median_stats'].loc['MERGED', 'deletions']:.2f}")

        report.append(f"- PRs fechados sem merge (CLOSED):")
        report.append(f"  - Arquivos alterados: {results['median_stats'].loc['CLOSED', 'files_changed']:.2f}")
        report.append(f"  - Linhas adicionadas: {results['median_stats'].loc['CLOSED', 'additions']:.2f}")
        report.append(f"  - Linhas removidas: {results['median_stats'].loc['CLOSED', 'deletions']:.2f}")

    # RQ 02
    report.append("\n### RQ 02: Relação entre o tempo de análise dos PRs e o feedback final das revisões")

    if "time_vs_status" in all_results:
        results = all_results["time_vs_status"]

        report.append("\n**Correlação entre tempo de análise e status:**")
        report.append(f"- Coeficiente de correlação: {results['time_vs_status']['correlation']:.4f}")
        report.append(f"- P-valor: {results['time_vs_status']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['time_vs_status']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['time_vs_status']['significant'] else 'Não'}")

        # Adicionar visualizações
        report.append(f"\n![Distribuição do Tempo de Análise por Status](data/visualizations/rq02_time_boxplot.png)")
        report.append(f"\n![Histograma do Tempo de Análise por Status](data/visualizations/rq02_time_histogram.png)")

        report.append("\n**Estatísticas descritivas (medianas):**")
        report.append(
            f"- PRs mesclados (MERGED): {results['median_stats'].loc['MERGED', 'time_to_close_hours']:.2f} horas")
        report.append(
            f"- PRs fechados sem merge (CLOSED): {results['median_stats'].loc['CLOSED', 'time_to_close_hours']:.2f} horas")

    # RQ 03
    report.append("\n### RQ 03: Relação entre a descrição dos PRs e o feedback final das revisões")

    if "description_vs_status" in all_results:
        results = all_results["description_vs_status"]

        report.append("\n**Correlação entre tamanho da descrição e status:**")
        report.append(f"- Coeficiente de correlação: {results['description_vs_status']['correlation']:.4f}")
        report.append(f"- P-valor: {results['description_vs_status']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['description_vs_status']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['description_vs_status']['significant'] else 'Não'}")

        # Adicionar visualizações
        report.append(
            f"\n![Distribuição do Tamanho da Descrição por Status](data/visualizations/rq03_description_boxplot.png)")
        report.append(f"\n![Mediana do Tamanho da Descrição por Status](data/visualizations/rq03_description_bars.png)")

        report.append("\n**Estatísticas descritivas (medianas):**")
        report.append(
            f"- PRs mesclados (MERGED): {results['median_stats'].loc['MERGED', 'body_length']:.2f} caracteres")
        report.append(
            f"- PRs fechados sem merge (CLOSED): {results['median_stats'].loc['CLOSED', 'body_length']:.2f} caracteres")

    # RQ 04
    report.append("\n### RQ 04: Relação entre as interações nos PRs e o feedback final das revisões")

    if "interactions_vs_status" in all_results:
        results = all_results["interactions_vs_status"]

        # Adicionar visualização principal
        report.append("\n**Correlação entre métricas de interação e status:**")
        report.append(f"\n![Correlação entre Interações e Status](data/visualizations/rq04_correlation.png)")

        report.append("\n**Correlação entre número de participantes e status:**")
        report.append(f"- Coeficiente de correlação: {results['participants_vs_status']['correlation']:.4f}")
        report.append(f"- P-valor: {results['participants_vs_status']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['participants_vs_status']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['participants_vs_status']['significant'] else 'Não'}")

        # Adicionar visualização de participantes
        report.append(
            f"\n![Distribuição de Participantes por Status](data/visualizations/rq04_participant_count_boxplot.png)")

        report.append("\n**Correlação entre número de comentários e status:**")
        report.append(f"- Coeficiente de correlação: {results['comments_vs_status']['correlation']:.4f}")
        report.append(f"- P-valor: {results['comments_vs_status']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['comments_vs_status']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['comments_vs_status']['significant'] else 'Não'}")

        # Adicionar visualização de comentários
        report.append(f"\n![Distribuição de Comentários por Status](data/visualizations/rq04_comments_boxplot.png)")

        report.append("\n**Correlação entre número de comentários de revisão e status:**")
        report.append(f"- Coeficiente de correlação: {results['review_comments_vs_status']['correlation']:.4f}")
        report.append(f"- P-valor: {results['review_comments_vs_status']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['review_comments_vs_status']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['review_comments_vs_status']['significant'] else 'Não'}")

        # Adicionar visualização de comentários de revisão
        report.append(
            f"\n![Distribuição de Comentários de Revisão por Status](data/visualizations/rq04_review_comments_boxplot.png)")

        report.append("\n**Estatísticas descritivas (medianas):**")
        report.append(f"- PRs mesclados (MERGED):")
        report.append(f"  - Participantes: {results['median_stats'].loc['MERGED', 'participant_count']:.2f}")
        report.append(f"  - Comentários: {results['median_stats'].loc['MERGED', 'comments']:.2f}")
        report.append(f"  - Comentários de revisão: {results['median_stats'].loc['MERGED', 'review_comments']:.2f}")

        report.append(f"- PRs fechados sem merge (CLOSED):")
        report.append(f"  - Participantes: {results['median_stats'].loc['CLOSED', 'participant_count']:.2f}")
        report.append(f"  - Comentários: {results['median_stats'].loc['CLOSED', 'comments']:.2f}")
        report.append(f"  - Comentários de revisão: {results['median_stats'].loc['CLOSED', 'review_comments']:.2f}")

    # RQ 05
    report.append("\n### RQ 05: Relação entre o tamanho dos PRs e o número de revisões realizadas")

    if "size_vs_reviews" in all_results:
        results = all_results["size_vs_reviews"]

        # Adicionar visualização principal
        report.append("\n**Correlação entre métricas de tamanho e número de revisões:**")
        report.append(
            f"\n![Correlação entre Tamanho dos PRs e Número de Revisões](data/visualizations/rq05_correlation.png)")

        report.append("\n**Correlação entre número de arquivos alterados e número de revisões:**")
        report.append(f"- Coeficiente de correlação: {results['files_vs_reviews']['correlation']:.4f}")
        report.append(f"- P-valor: {results['files_vs_reviews']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['files_vs_reviews']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['files_vs_reviews']['significant'] else 'Não'}")

        # Adicionar visualização
        report.append(
            f"\n![Relação entre Número de Arquivos e Revisões](data/visualizations/rq05_files_changed_scatter.png)")

        report.append("\n**Correlação entre linhas adicionadas e número de revisões:**")
        report.append(f"- Coeficiente de correlação: {results['additions_vs_reviews']['correlation']:.4f}")
        report.append(f"- P-valor: {results['additions_vs_reviews']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['additions_vs_reviews']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['additions_vs_reviews']['significant'] else 'Não'}")

        # Adicionar visualização
        report.append(
            f"\n![Relação entre Linhas Adicionadas e Revisões](data/visualizations/rq05_additions_scatter.png)")

        report.append("\n**Correlação entre linhas removidas e número de revisões:**")
        report.append(f"- Coeficiente de correlação: {results['deletions_vs_reviews']['correlation']:.4f}")
        report.append(f"- P-valor: {results['deletions_vs_reviews']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['deletions_vs_reviews']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['deletions_vs_reviews']['significant'] else 'Não'}")

        # Adicionar visualização
        report.append(f"\n![Relação entre Linhas Removidas e Revisões](data/visualizations/rq05_deletions_scatter.png)")

    # RQ 06
    report.append("\n### RQ 06: Relação entre o tempo de análise dos PRs e o número de revisões realizadas")

    if "time_vs_reviews" in all_results:
        results = all_results["time_vs_reviews"]

        report.append("\n**Correlação entre tempo de análise e número de revisões:**")
        report.append(f"- Coeficiente de correlação: {results['time_vs_reviews']['correlation']:.4f}")
        report.append(f"- P-valor: {results['time_vs_reviews']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['time_vs_reviews']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['time_vs_reviews']['significant'] else 'Não'}")

        # Adicionar visualizações
        report.append(f"\n![Relação entre Tempo de Análise e Revisões](data/visualizations/rq06_time_scatter.png)")
        report.append(f"\n![Média de Revisões por Faixa de Tempo](data/visualizations/rq06_time_bins.png)")

    # RQ 07
    report.append("\n### RQ 07: Relação entre a descrição dos PRs e o número de revisões realizadas")

    if "description_vs_reviews" in all_results:
        results = all_results["description_vs_reviews"]

        report.append("\n**Correlação entre tamanho da descrição e número de revisões:**")
        report.append(f"- Coeficiente de correlação: {results['description_vs_reviews']['correlation']:.4f}")
        report.append(f"- P-valor: {results['description_vs_reviews']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['description_vs_reviews']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['description_vs_reviews']['significant'] else 'Não'}")

        # Adicionar visualizações
        report.append(
            f"\n![Relação entre Tamanho da Descrição e Revisões](data/visualizations/rq07_description_scatter.png)")
        report.append(f"\n![Média de Revisões por Tamanho de Descrição](data/visualizations/rq07_desc_bins.png)")

    # RQ 08
    report.append("\n### RQ 08: Relação entre as interações nos PRs e o número de revisões realizadas")

    if "interactions_vs_reviews" in all_results:
        results = all_results["interactions_vs_reviews"]

        # Adicionar visualização principal
        report.append("\n**Correlação entre métricas de interação e número de revisões:**")
        report.append(
            f"\n![Correlação entre Interações e Número de Revisões](data/visualizations/rq08_correlation.png)")

        report.append("\n**Correlação entre número de participantes e número de revisões:**")
        report.append(f"- Coeficiente de correlação: {results['participants_vs_reviews']['correlation']:.4f}")
        report.append(f"- P-valor: {results['participants_vs_reviews']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['participants_vs_reviews']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['participants_vs_reviews']['significant'] else 'Não'}")

        # Adicionar visualização
        report.append(
            f"\n![Relação entre Número de Participantes e Revisões](data/visualizations/rq08_participant_count_scatter.png)")

        report.append("\n**Correlação entre número de comentários e número de revisões:**")
        report.append(f"- Coeficiente de correlação: {results['comments_vs_reviews']['correlation']:.4f}")
        report.append(f"- P-valor: {results['comments_vs_reviews']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['comments_vs_reviews']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['comments_vs_reviews']['significant'] else 'Não'}")

        # Adicionar visualização
        report.append(
            f"\n![Relação entre Número de Comentários e Revisões](data/visualizations/rq08_comments_scatter.png)")

        report.append("\n**Correlação entre número de comentários de revisão e número de revisões:**")
        report.append(f"- Coeficiente de correlação: {results['review_comments_vs_reviews']['correlation']:.4f}")
        report.append(f"- P-valor: {results['review_comments_vs_reviews']['p_value']:.4e}")
        report.append(f"- Interpretação: {results['review_comments_vs_reviews']['interpretation']}")
        report.append(
            f"- Estatisticamente significativo: {'Sim' if results['review_comments_vs_reviews']['significant'] else 'Não'}")

        # Adicionar visualização
        report.append(
            f"\n![Relação entre Número de Comentários de Revisão e Revisões](data/visualizations/rq08_review_comments_scatter.png)")

    # Discussão
    report.append("\n## Discussão")
    report.append("\nNesta seção, discutimos os resultados obtidos em relação às nossas hipóteses iniciais.")

    # RQ 01
    report.append("\n### RQ 01: Relação entre o tamanho dos PRs e o feedback final das revisões")
    report.append("\nHipótese: PRs menores têm maior probabilidade de serem aprovados.")
    if "size_vs_status" in all_results:
        results = all_results["size_vs_status"]

        if results['files_vs_status']['correlation'] < 0 and results['files_vs_status']['significant']:
            report.append("\nOs resultados suportam nossa hipótese. Encontramos uma correlação " +
                          results['files_vs_status']['interpretation'].lower() +
                          " e estatisticamente significativa entre o número de arquivos alterados e a aprovação do PR. " +
                          "PRs com menos arquivos alterados têm maior probabilidade de serem aprovados.")
        else:
            report.append(
                "\nOs resultados não suportam completamente nossa hipótese. A correlação entre o tamanho do PR e sua aprovação não foi tão forte ou significativa como esperávamos.")

    # RQ 02
    report.append("\n### RQ 02: Relação entre o tempo de análise dos PRs e o feedback final das revisões")
    report.append(
        "\nHipótese: PRs que levam mais tempo para serem analisados têm menor probabilidade de serem aprovados.")
    if "time_vs_status" in all_results:
        results = all_results["time_vs_status"]

        if results['time_vs_status']['correlation'] < 0 and results['time_vs_status']['significant']:
            report.append("\nOs resultados suportam nossa hipótese. Encontramos uma correlação " +
                          results['time_vs_status']['interpretation'].lower() +
                          " e estatisticamente significativa entre o tempo de análise e a aprovação do PR. " +
                          "PRs que levam mais tempo para serem analisados têm menor probabilidade de serem aprovados.")
        else:
            report.append(
                "\nOs resultados não suportam completamente nossa hipótese. A correlação entre o tempo de análise e a aprovação do PR não foi tão forte ou significativa como esperávamos.")

    # RQ 03
    report.append("\n### RQ 03: Relação entre a descrição dos PRs e o feedback final das revisões")
    report.append("\nHipótese: PRs com descrições mais detalhadas têm maior probabilidade de serem aprovados.")
    if "description_vs_status" in all_results:
        results = all_results["description_vs_status"]

        if results['description_vs_status']['correlation'] > 0 and results['description_vs_status']['significant']:
            report.append("\nOs resultados suportam nossa hipótese. Encontramos uma correlação " +
                          results['description_vs_status']['interpretation'].lower() +
                          " e estatisticamente significativa entre o tamanho da descrição e a aprovação do PR. " +
                          "PRs com descrições mais detalhadas têm maior probabilidade de serem aprovados.")
        else:
            report.append(
                "\nOs resultados não suportam completamente nossa hipótese. A correlação entre o tamanho da descrição e a aprovação do PR não foi tão forte ou significativa como esperávamos.")

    # RQ 04
    report.append("\n### RQ 04: Relação entre as interações nos PRs e o feedback final das revisões")
    report.append("\nHipótese: PRs com mais interações têm maior probabilidade de serem aprovados.")
    if "interactions_vs_status" in all_results:
        results = all_results["interactions_vs_status"]

        if (results['participants_vs_status']['correlation'] > 0 and results['participants_vs_status'][
            'significant']) or \
                (results['comments_vs_status']['correlation'] > 0 and results['comments_vs_status']['significant']) or \
                (results['review_comments_vs_status']['correlation'] > 0 and results['review_comments_vs_status'][
                    'significant']):
            report.append(
                "\nOs resultados suportam parcialmente nossa hipótese. Encontramos correlações significativas entre algumas métricas de interação e a aprovação do PR. " +
                "PRs com mais interações tendem a ter maior probabilidade de serem aprovados, possivelmente porque problemas são identificados e resolvidos durante o processo de revisão.")
        else:
            report.append(
                "\nOs resultados não suportam nossa hipótese. As correlações entre as métricas de interação e a aprovação do PR não foram tão fortes ou significativas como esperávamos.")

    # RQ 05
    report.append("\n### RQ 05: Relação entre o tamanho dos PRs e o número de revisões realizadas")
    report.append("\nHipótese: PRs maiores requerem mais revisões.")
    if "size_vs_reviews" in all_results:
        results = all_results["size_vs_reviews"]

        if (results['files_vs_reviews']['correlation'] > 0 and results['files_vs_reviews']['significant']) or \
                (results['additions_vs_reviews']['correlation'] > 0 and results['additions_vs_reviews'][
                    'significant']) or \
                (results['deletions_vs_reviews']['correlation'] > 0 and results['deletions_vs_reviews']['significant']):
            report.append(
                "\nOs resultados suportam nossa hipótese. Encontramos correlações significativas entre o tamanho do PR e o número de revisões realizadas. " +
                "PRs maiores tendem a requerer mais revisões, possivelmente porque contêm mais código a ser analisado e mais problemas potenciais a serem identificados.")
        else:
            report.append(
                "\nOs resultados não suportam completamente nossa hipótese. As correlações entre o tamanho do PR e o número de revisões não foram tão fortes ou significativas como esperávamos.")

    # Restante das discussões
    report.append("\n### RQ 06: Relação entre o tempo de análise dos PRs e o número de revisões realizadas")
    report.append("\nHipótese: PRs que levam mais tempo para serem analisados têm mais revisões.")
    if "time_vs_reviews" in all_results:
        results = all_results["time_vs_reviews"]

        if results['time_vs_reviews']['correlation'] > 0 and results['time_vs_reviews']['significant']:
            report.append("\nOs resultados suportam nossa hipótese. Encontramos uma correlação " +
                          results['time_vs_reviews']['interpretation'].lower() +
                          " e estatisticamente significativa entre o tempo de análise e o número de revisões. " +
                          "PRs que levam mais tempo para serem analisados têm mais revisões, possivelmente porque revisões adicionais são necessárias para resolver problemas identificados.")
        else:
            report.append(
                "\nOs resultados não suportam completamente nossa hipótese. A correlação entre o tempo de análise e o número de revisões não foi tão forte ou significativa como esperávamos.")

    # RQ 07
    report.append("\n### RQ 07: Relação entre a descrição dos PRs e o número de revisões realizadas")
    report.append("\nHipótese: PRs com descrições mais detalhadas têm menos revisões.")
    if "description_vs_reviews" in all_results:
        results = all_results["description_vs_reviews"]

        if results['description_vs_reviews']['correlation'] < 0 and results['description_vs_reviews']['significant']:
            report.append("\nOs resultados suportam nossa hipótese. Encontramos uma correlação " +
                          results['description_vs_reviews']['interpretation'].lower() +
                          " e estatisticamente significativa entre o tamanho da descrição e o número de revisões. " +
                          "PRs com descrições mais detalhadas têm menos revisões, possivelmente porque os revisores entendem melhor o propósito e o contexto do PR.")
        else:
            report.append(
                "\nOs resultados não suportam nossa hipótese. A correlação entre o tamanho da descrição e o número de revisões não foi negativa ou significativa como esperávamos.")

    # RQ 08
    report.append("\n### RQ 08: Relação entre as interações nos PRs e o número de revisões realizadas")
    report.append("\nHipótese: PRs com mais interações têm mais revisões.")
    if "interactions_vs_reviews" in all_results:
        results = all_results["interactions_vs_reviews"]

        if (results['participants_vs_reviews']['correlation'] > 0 and results['participants_vs_reviews'][
            'significant']) or \
                (results['comments_vs_reviews']['correlation'] > 0 and results['comments_vs_reviews']['significant']) or \
                (results['review_comments_vs_reviews']['correlation'] > 0 and results['review_comments_vs_reviews'][
                    'significant']):
            report.append(
                "\nOs resultados suportam nossa hipótese. Encontramos correlações significativas entre as métricas de interação e o número de revisões. " +
                "PRs com mais interações têm mais revisões, possivelmente porque cada revisão gera comentários e discussões que podem levar a revisões adicionais.")
        else:
            report.append(
                "\nOs resultados não suportam completamente nossa hipótese. As correlações entre as métricas de interação e o número de revisões não foram tão fortes ou significativas como esperávamos.")

    # Conclusão
    report.append("\n## Conclusão")
    report.append(
        "\nEste estudo analisou a relação entre diversas características dos PRs e seu feedback final, bem como o número de revisões realizadas. Os resultados fornecem insights valiosos sobre como melhorar a chance de aprovação de PRs e otimizar o processo de code review em projetos open source.")

    report.append("\nCom base nos resultados, podemos sugerir as seguintes práticas para melhorar a aprovação de PRs:")
    report.append("\n1. Manter os PRs pequenos, afetando poucos arquivos e com poucas linhas alteradas.")
    report.append("2. Incluir descrições detalhadas e claras, explicando o propósito e o contexto do PR.")
    report.append(
        "3. Promover interações construtivas durante o processo de revisão, respondendo prontamente aos comentários.")
    report.append(
        "4. Evitar PRs que levem muito tempo para serem analisados, dividindo mudanças grandes em PRs menores e mais focados.")

    report.append(
        "\nEsperamos que estes insights ajudem desenvolvedores e mantenedores de projetos open source a otimizar seus processos de code review, melhorando a qualidade do código e a experiência dos contribuidores.")

    # Escrever o relatório em um arquivo
    with open(output_file, "w") as f:
        f.write("\n".join(report))

    print(f"Relatório gerado com sucesso em {output_file}")


def main():
    # Criar diretório para visualizações
    os.makedirs("data/visualizations", exist_ok=True)

    # Carregar os dados
    df = load_data("data/collected_prs.csv")
    print(f"Dados carregados com sucesso. Total de {len(df)} PRs.")

    # Analisar as questões de pesquisa
    all_results = {}

    # Dimensão A: Feedback Final das Revisões (Status do PR)
    print("Analisando RQ 01: Tamanho vs. Status...")
    all_results["size_vs_status"] = analyze_size_vs_status(df)

    print("Analisando RQ 02: Tempo vs. Status...")
    all_results["time_vs_status"] = analyze_time_vs_status(df)

    print("Analisando RQ 03: Descrição vs. Status...")
    all_results["description_vs_status"] = analyze_description_vs_status(df)

    print("Analisando RQ 04: Interações vs. Status...")
    all_results["interactions_vs_status"] = analyze_interactions_vs_status(df)

    # Dimensão B: Número de Revisões
    print("Analisando RQ 05: Tamanho vs. Revisões...")
    all_results["size_vs_reviews"] = analyze_size_vs_reviews(df)

    print("Analisando RQ 06: Tempo vs. Revisões...")
    all_results["time_vs_reviews"] = analyze_time_vs_reviews(df)

    print("Analisando RQ 07: Descrição vs. Revisões...")
    all_results["description_vs_reviews"] = analyze_description_vs_reviews(df)

    print("Analisando RQ 08: Interações vs. Revisões...")
    all_results["interactions_vs_reviews"] = analyze_interactions_vs_reviews(df)

    # Gerar relatório
    print("Gerando relatório...")
    generate_report(all_results, "data/report.md")

    print("Análise concluída!")


if __name__ == "__main__":
    main()