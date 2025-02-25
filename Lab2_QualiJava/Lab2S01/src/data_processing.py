import pandas as pd
import os


def summarize_metrics(metrics_dir):
    """
    Processa e sumariza os resultados das métricas.
    """
    # Caminhos para os arquivos
    class_csv_path = os.path.join(metrics_dir, "class.csv")
    method_csv_path = os.path.join(metrics_dir, "method.csv")

    # Verifica se os arquivos existem e não estão vazios
    if not os.path.exists(class_csv_path) or os.path.getsize(class_csv_path) == 0:
        raise FileNotFoundError(f"Arquivo 'class.csv' ausente ou vazio em: {class_csv_path}")
    if not os.path.exists(method_csv_path) or os.path.getsize(method_csv_path) == 0:
        raise FileNotFoundError(f"Arquivo 'method.csv' ausente ou vazio em: {method_csv_path}")

    # Leitura dos arquivos CSV
    class_metrics = pd.read_csv(class_csv_path)
    method_metrics = pd.read_csv(method_csv_path)

    # Verifica se os DataFrames estão vazios
    if class_metrics.empty or "cbo" not in class_metrics or "dit" not in class_metrics or "lcom" not in class_metrics:
        raise ValueError(f"O arquivo 'class.csv' não possui as colunas esperadas ou está vazio.")

    # Calcula as métricas a partir dos dados disponíveis
    summary = {
        "CBO_mean": class_metrics["cbo"].mean(),
        "DIT_mean": class_metrics["dit"].mean(),
        "LCOM_mean": class_metrics["lcom"].mean()
    }

    return pd.DataFrame([summary])


if __name__ == "__main__":
    METRICS_DIR = "data/processed/metrics"
    try:
        summary = summarize_metrics(METRICS_DIR)
        summary.to_csv("data/results/summary.csv", index=False)
        print("Resumo criado com sucesso e salvo em: data/results/summary.csv")
    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except ValueError as e:
        print(f"Erro nos dados: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
