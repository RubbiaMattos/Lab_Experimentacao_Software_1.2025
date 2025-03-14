import subprocess
import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def clone_repositories():
    logging.info("Iniciando a clonagem dos repositórios...")
    subprocess.run(["python", "automacao_clone.py"], check=True)

def coletar_dados():
    logging.info("Coletando dados dos repositórios...")
    subprocess.run(["python", "coletar_dados.py"], check=True)

def analisar_dados():
    logging.info("Analisando os dados coletados...")
    subprocess.run(["python", "analisar_dados.py"], check=True)

def main():
    parser = argparse.ArgumentParser(description="Pipeline completo do laboratório")
    parser.add_argument("--step", type=str, choices=["clone", "coletar", "analisar", "all"], default="all",
                        help="Escolha a etapa: clone, coletar, analisar, ou all para executar todas.")
    args = parser.parse_args()

    if args.step == "clone":
        clone_repositories()
    elif args.step == "coletar":
        coletar_dados()
    elif args.step == "analisar":
        analisar_dados()
    elif args.step == "all":
        clone_repositories()
        coletar_dados()
        analisar_dados()

if __name__ == "__main__":
    main()
