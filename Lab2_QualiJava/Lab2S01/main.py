import subprocess
import argparse
import logging
import os
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_DIR = os.path.dirname(__file__)

def run_subprocess(script_name):
    script_path = os.path.join(BASE_DIR, script_name)
    subprocess.run(["python", script_path])

def buscar_repositorios():
    logging.info("===== 🌐 1ª ETAPA: BUSCAR REPOSITÓRIOS =====")
    start = time.time()
    run_subprocess('coleta_repositorios.py')
    end = time.time()
    logging.info(f"✅ Busca finalizada em {end - start:.2f} segundos\n")

def clone_repositories():
    logging.info("===== 🐙 2ª ETAPA: CLONAR REPOSITÓRIOS =====")
    start = time.time()
    run_subprocess('automacao_clone.py')
    end = time.time()
    logging.info(f"✅ Clonagem finalizada em {end - start:.2f} segundos\n")

def coletar_dados():
    logging.info("===== 📥 3ª ETAPA: COLETAR DADOS =====")
    start = time.time()
    run_subprocess('coletar_dados.py')
    end = time.time()
    logging.info(f"✅ Coleta de dados finalizada em {end - start:.2f} segundos\n")

def analisar_dados():
    logging.info("===== 📊 4ª ETAPA: ANALISAR DADOS =====")
    start = time.time()
    run_subprocess('analisar_dados.py')
    end = time.time()
    logging.info(f"✅ Análise finalizada em {end - start:.2f} segundos\n")

def main():
    parser = argparse.ArgumentParser(description="🚀 Pipeline completo do laboratório")
    parser.add_argument(
        "--step",
        type=str,
        choices=["buscar", "clone", "coletar", "analisar", "all"],
        default="all",
        help="Escolha a etapa: buscar 🌐, clone 🐙, coletar 📥, analisar 📊 ou all 🔄 para executar tudo."
    )
    args = parser.parse_args()

    if args.step == "buscar":
        buscar_repositorios()
    elif args.step == "clone":
        clone_repositories()
    elif args.step == "coletar":
        coletar_dados()
    elif args.step == "analisar":
        analisar_dados()
    elif args.step == "all":
        logging.info("🔄 Executando o pipeline completo...")
        buscar_repositorios()
        clone_repositories()
        coletar_dados()
        analisar_dados()
        logging.info("✅ Pipeline finalizado com sucesso!")

if __name__ == "__main__":
    main()
