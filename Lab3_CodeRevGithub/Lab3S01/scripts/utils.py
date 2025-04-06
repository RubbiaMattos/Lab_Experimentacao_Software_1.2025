import os
import sys
import numpy as np
from scipy import stats
import csv
import json
from collections import Counter

BASE_DIR = os.path.join("Lab3_CodeRevGithub", "Lab3S01")
DATA_DIR = os.path.join(BASE_DIR, "data")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from config_token import configurar_token

TOKEN = configurar_token()

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


def converter_csv_json():

    # Caminho dos arquivos
    csv_file_path = os.path.join(DATA_DIR, "collected_prs.csv")
    json_file_path = os.path.join(DATA_DIR, "collected_prs.json")
    
   # Leitura do CSV e escrita no JSON
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file, \
        open(json_file_path, mode='w', encoding='utf-8') as json_file:
        
        dados = list(csv.DictReader(csv_file))
        json.dump(dados, json_file, indent=4, ensure_ascii=False)
        print(f"Arquivo convertido e salvo como {json_file_path}")

    # Leitura do JSON e contagem de valores da chave "repo_name"
    with open(json_file_path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    repo_counter = Counter(obj["repo_name"] for obj in dados if "repo_name" in obj)

    print(f"\nNúmero total de objetos no JSON: {len(dados)}")
    print("\nFrequência dos valores da chave 'repo_name':")
    for i, (repo, count) in enumerate(repo_counter.items(), start=1):
        print(f"{i}. {repo}: {count}")
