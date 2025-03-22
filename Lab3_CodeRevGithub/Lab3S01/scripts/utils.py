import os
import pandas as pd
import numpy as np
from scipy import stats


def get_github_token():
    token = "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"  # Insira seu token diretamente aqui
    if not token:
        raise ValueError("Token do GitHub não definido")
    return token


def calculate_correlation(data, x_column, y_column, method='spearman'):
    """
    Calcula a correlação entre duas variáveis usando o método especificado.

    Args:
        data (pd.DataFrame): DataFrame contendo os dados
        x_column (str): Nome da coluna X
        y_column (str): Nome da coluna Y
        method (str): Método de correlação ('spearman' ou 'pearson')

    Returns:
        tuple: (coeficiente de correlação, valor-p)
    """
    # Remove valores nulos
    valid_data = data[[x_column, y_column]].dropna()

    if len(valid_data) < 2:
        return np.nan, np.nan

    if method == 'spearman':
        return stats.spearmanr(valid_data[x_column], valid_data[y_column])
    elif method == 'pearson':
        return stats.pearsonr(valid_data[x_column], valid_data[y_column])
    else:
        raise ValueError(f"Método de correlação inválido: {method}")


def interpret_correlation(corr_val):
    """
    Interpreta o valor de correlação.

    Args:
        corr_val (float): Valor da correlação

    Returns:
        str: Interpretação da correlação
    """
    abs_corr = abs(corr_val)

    if np.isnan(corr_val):
        return "Indefinida"
    elif abs_corr < 0.1:
        return "Insignificante"
    elif abs_corr < 0.3:
        return "Fraca"
    elif abs_corr < 0.5:
        return "Moderada"
    elif abs_corr < 0.7:
        return "Forte"
    else:
        return "Muito forte"


def check_correlation_significance(p_value, alpha=0.05):
    """
    Verifica se a correlação é estatisticamente significativa.

    Args:
        p_value (float): Valor-p da correlação
        alpha (float): Nível de significância

    Returns:
        bool: True se a correlação for significativa, False caso contrário
    """
    return p_value < alpha