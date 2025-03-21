import subprocess
import argparse
import logging
import os
import time

# Evita duplicação de logs
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
)

BASE_DIR = os.path.dirname(__file__)

def formatar_tempo(segundos):
    horas, resto = divmod(int(segundos), 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def run_subprocess(script_name):
    """
    🔄 Executa um subprocesso chamando o script indicado.
    """
    script_path = os.path.join(BASE_DIR, script_name)
    subprocess.run(["python", script_path])

def buscar_repositorios():
    """
    🌐 Etapa 1: Buscar repositórios da API.
    """
    logging.info("===== 🌐 1ª ETAPA: BUSCAR REPOSITÓRIOS =====\n")
    start = time.time()
    run_subprocess('coleta_repositorios.py')
    end = time.time()
    logging.info(f"✅ Busca finalizada em {formatar_tempo(end - start)} \n")

def clone_repositories():
    """
    🐙 Etapa 2: Clonar repositórios e conferir o total.
    """
    logging.info("===== 🐙 2ª ETAPA: CLONAR REPOSITÓRIOS =====\n")
    start = time.time()
    run_subprocess("automacao_clone.py")
    end = time.time()
    logging.info(f"✅ Clonagem finalizada em {formatar_tempo(end - start)} \n")

def coletar_dados():
    """
    📥 Etapa 3: Coletar dados e métricas CK.
    """
    logging.info("===== 📥 3ª ETAPA: COLETAR DADOS =====\n")
    start = time.time()
    run_subprocess('coletar_dados.py')
    end = time.time()
    logging.info(f"✅ Coleta de dados finalizada em {formatar_tempo(end - start)} \n")

def analisar_dados():
    """
    📊 Etapa 4: Analisar dados coletados.
    """
    logging.info("===== 📊 4ª ETAPA: ANALISAR DADOS =====\n")
    start = time.time()
    run_subprocess('analisar_dados.py')
    end = time.time()
    logging.info(f"✅ Análise finalizada em {formatar_tempo(end - start)} \n")

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
        logging.info("🔄 Executando o pipeline completo...\n")
        buscar_repositorios()
        clone_repositories()
        coletar_dados()
        analisar_dados()
        logging.info("🎉 Pipeline finalizado com sucesso!")

if __name__ == "__main__":
    main()