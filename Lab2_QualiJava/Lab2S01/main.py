import subprocess
import argparse
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_DIR = os.path.dirname(__file__)

def run_subprocess(script_name):
    script_path = os.path.join(BASE_DIR, script_name)
    result = subprocess.run(["python", script_path], capture_output=True, text=True)

    if result.stdout:
        # Joga o stdout do script direto no logger
        for line in result.stdout.strip().split('\n'):
            logging.info(line)
    if result.stderr:
        for line in result.stderr.strip().split('\n'):
            logging.error(line)

def clone_repositories():
    logging.info("🐙 Iniciando a clonagem dos repositórios...")
    run_subprocess('automacao_clone.py')

def coletar_dados():
    logging.info("📥 Coletando dados dos repositórios...")
    run_subprocess('coletar_dados.py')

def analisar_dados():
    logging.info("📊 Analisando os dados coletados...")
    run_subprocess('analisar_dados.py')

def main():
    parser = argparse.ArgumentParser(description="🚀 Pipeline completo do laboratório")
    parser.add_argument(
        "--step",
        type=str,
        choices=["clone", "coletar", "analisar", "all"],
        default="all",
        help="Escolha a etapa: clone 🐙, coletar 📥, analisar 📊 ou all 🔄 para executar todas."
    )
    args = parser.parse_args()

    if args.step == "clone":
        clone_repositories()
    elif args.step == "coletar":
        coletar_dados()
    elif args.step == "analisar":
        analisar_dados()
    elif args.step == "all":
        logging.info("🔄 Executando o pipeline completo...")
        clone_repositories()
        coletar_dados()
        analisar_dados()
        logging.info("✅ Pipeline finalizado com sucesso!")

if __name__ == "__main__":
    main()
