import os
import pandas as pd
import numpy as np
from scipy import stats
from dotenv import load_dotenv

# Carrega automaticamente variáveis do .env
load_dotenv()


def get_github_token():
    """
    Retorna o token do GitHub da variável de ambiente GITHUB_TOKEN.
    
    Returns:
        str: Token de acesso ao GitHub
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("Token do GitHub não definido. Verifique seu arquivo .env.")
    return token


def calculate_correlation(data, x_column, y_column, method='spearman'):
    """
    Calcula a correlação entre duas variáveis.

    Args:
        data (pd.DataFrame): DataFrame contendo os dados
        x_column (str): Nome da coluna X
        y_column (str): Nome da coluna Y
        method (str): Método de correlação ('spearman' ou 'pearson')

    Returns:
        tuple: (coeficiente de correlação, valor-p)
    """
    valid_data = data[[x_column, y_column]].dropna()

    if len(valid_data) < 2:
        return np.nan, np.nan

    try:
        if method == 'spearman':
            return stats.spearmanr(valid_data[x_column], valid_data[y_column])
        elif method == 'pearson':
            return stats.pearsonr(valid_data[x_column], valid_data[y_column])
        else:
            raise ValueError(f"Método de correlação inválido: {method}")
    except Exception as e:
        print(f"Erro ao calcular correlação: {e}")
        return np.nan, np.nan


def interpret_correlation(corr_val):
    """
    Interpreta a força da correlação com base em seu valor absoluto.

    Args:
        corr_val (float): Valor da correlação

    Returns:
        str: Interpretação textual
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
        p_value (float): Valor-p retornado pela correlação
        alpha (float): Nível de significância

    Returns:
        bool: True se significativa, False se não
    """
    if np.isnan(p_value):
        return False
    return p_value < alpha
