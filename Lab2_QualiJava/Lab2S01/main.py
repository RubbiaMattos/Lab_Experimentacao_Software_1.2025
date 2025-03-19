import subprocess
import argparse
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_DIR = os.path.dirname(__file__)

def clone_repositories():
    logging.info("🐙 Iniciando a clonagem dos repositórios...")
    script_path = os.path.join(BASE_DIR, 'automacao_clone.py')
    subprocess.run(["python", script_path], check=True)

def coletar_dados():
    logging.info("📥 Coletando dados dos repositórios...")
    script_path = os.path.join(BASE_DIR, 'coletar_dados.py')
    subprocess.run(["python", script_path], check=True)

def analisar_dados():
    logging.info("📊 Analisando os dados coletados...")
    script_path = os.path.join(BASE_DIR, 'analisar_dados.py')
    subprocess.run(["python", script_path], check=True)

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
