import os
import subprocess


def run_ck_tool(repo_path, output_dir, use_jars=False, max_files_per_partition=0, include_variable_metrics=False,
                ignored_dirs=None):
    """
    Executa a ferramenta CK em um repositório de código Java.

    :param repo_path: Caminho para o diretório do repositório que contém os arquivos .java.
    :param output_dir: Caminho para o diretório onde os arquivos CSV serão gerados.
    :param use_jars: Se o CK deve considerar dependências externas (jars).
    :param max_files_per_partition: Número máximo de arquivos por partição (use 0 para automático).
    :param include_variable_metrics: Se métricas de variáveis e campos devem ser incluídas.
    :param ignored_dirs: Lista de diretórios a serem ignorados (opcional).
    """
    # Certifique-se de que o diretório de saída existe
    os.makedirs(output_dir, exist_ok=True)

    # Caminho para o ck.jar
    jar_path = "C:\\ck\\target\\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"

    # Construa o comando
    command = [
        "java", "-jar", jar_path,
        repo_path,
        "true" if use_jars else "false",
        str(max_files_per_partition),
        "true" if include_variable_metrics else "false",
        output_dir
    ]

    # Adicionar diretórios ignorados, caso existam
    if ignored_dirs:
        command.extend(ignored_dirs)

    # Informações de debug
    print(f"Executando CK no repositório: {repo_path}")
    print(f"Comando: {' '.join(command)}")

    try:
        # Executando o comando
        subprocess.run(command, check=True)
        print("CK executado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar CK: {e}")
    except FileNotFoundError:
        print("Erro: Certifique-se de que o Java está instalado e configurado no PATH.")
    except Exception as e:
        print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    # Substitua pelo caminho do repositório que você deseja analisar
    REPO_PATH = "C:\\ck\\src\\main\\java\\com\\github\\mauricioaniche\\ck\\ck.java"

    # Caminho para o diretório onde os resultados serão salvos
    OUTPUT_DIR = "data/processed/metrics"

    # Diretórios opcionais a serem ignorados
    IGNORED_DIRS = ["build/", "out/"]

    # Executa o CK no repositório especificado
    run_ck_tool(
        repo_path=REPO_PATH,
        output_dir=OUTPUT_DIR,
        use_jars=False,
        max_files_per_partition=0,
        include_variable_metrics=False,
        ignored_dirs=IGNORED_DIRS
    )