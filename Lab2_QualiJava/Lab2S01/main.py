import shutil
import subprocess
import argparse
import logging
import os
import time
from tqdm import tqdm
import stat

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
    script_path = os.path.join(BASE_DIR, script_name)
    subprocess.run(["python", script_path], check=True)

def buscar_repositorios():
    logging.info("===== 🌐 1ª ETAPA: BUSCAR REPOSITÓRIOS =====\n")
    start = time.time()
    run_subprocess('coleta_repositorios.py')
    end = time.time()
    logging.info(f"\033[1m\033[93m✅ Busca finalizada em {formatar_tempo(end - start)}\033[0m\n")
    print("=" * 120 + "\n")

def clone_repositories():
    logging.info("===== 🔙 2ª ETAPA: CLONAR REPOSITÓRIOS =====\n")
    start = time.time()
    run_subprocess("automacao_clone.py")
    end = time.time()
    logging.info(f"\033[1m\033[93m✅ Clonagem finalizada em {formatar_tempo(end - start)}\033[0m\n")
    print("=" * 120 + "\n")

def coletar_dados():
    logging.info("===== 📥 3ª ETAPA: COLETAR DADOS =====\n")
    start = time.time()
    run_subprocess('coletar_dados.py')
    end = time.time()
    logging.info(f"\033[1m\033[93m✅ Coleta de dados finalizada em {formatar_tempo(end - start)}\033[0m\n")
    print("=" * 120 + "\n")

def analisar_dados():
    logging.info("===== 📊 4ª ETAPA: ANALISAR DADOS =====\n")
    start = time.time()
    run_subprocess('analisar_dados.py')
    end = time.time()
    logging.info(f"\033[1m\033[93m✅ Análise finalizada em {formatar_tempo(end - start)}\033[0m\n")
    print("=" * 120 + "\n")

def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def limpar_conteudo_pasta(pasta):
    """Limpa somente as pastas dentro da pasta especificada."""
    if not os.path.exists(pasta):
        logging.warning(f"⚠️ Pasta {pasta} não encontrada para limpeza.")
        return

    itens = [item for item in os.listdir(pasta) if os.path.isdir(os.path.join(pasta, item))]  # Filtra apenas pastas
    
    # Se houver pastas, cria a barra de progresso
    if itens:
        with tqdm(total=len(itens), desc=f"{' ' * 37}🗑️  Limpando \033[92m{os.path.basename(pasta)}\033[0m", unit=" pasta") as pbar:
            for item in itens:
                item_path = os.path.join(pasta, item)
                try:
                    shutil.rmtree(item_path, onerror=remove_readonly)  # Remove a pasta
                    pbar.update(1)  # Atualiza a barra de progresso para cada pasta removida
                except Exception as e:
                    logging.warning(f"⚠️ Erro ao remover a pasta {item_path}: {e}")
    else:
        logging.info(f"📂 Pasta \033[92m{os.path.basename(pasta)}\033[0m está vazia, sem itens para limpar.")

def main():
    parser = argparse.ArgumentParser(description="🚀 Pipeline completo do laboratório")
    parser.add_argument(
        "--step",
        type=str,
        choices=["buscar", "clone", "coletar", "analisar", "all"],
        default="all",
        help="Escolha a etapa: buscar 🌐, clone 🔙, coletar 📥, analisar 📊 ou all 🔄 para executar tudo."
    )
    args = parser.parse_args()

    data_path = os.path.join(BASE_DIR, "data")
    repos_dir = r"C:\\Repos"

    if args.step == "all":
        print("\n⚠️   ATENÇÃO: Esta ação irá limpar o conteúdo das pastas 'data' e 'C:\\Repos'.\n")
        confirmacao = input("Deseja realmente limpar o conteúdo das pastas? (s/n): ").strip().lower()
        print("=" * 120)

        if confirmacao == "s":
            if os.path.exists(data_path):
                print(" ")
                logging.info(f"\033[4m\033[96m📝 Preparando Pasta \033[1m{os.path.basename(data_path)}\033[0m")
                logging.info("🗑️   Limpando o conteúdo da pasta de dados (\033[92mdata\033[0m) antes de rodar o pipeline...")
                limpar_conteudo_pasta(data_path)

            if os.path.exists(repos_dir):
                print(" ")
                logging.info(f"\033[4m\033[96m📝 Preparando Pasta \033[1m{os.path.basename(repos_dir)}\033[0m")
                logging.info(f"🪟   Alterando permissões da pasta \033[92m{repos_dir}\033[0m...")

                # Obtendo o nome do usuário atual
                try:
                    current_user = os.getlogin()  # Obtém o login do usuário no sistema
                except Exception:
                    import getpass
                    current_user = getpass.getuser()  # Como fallback, usa getpass para obter o nome do usuário

                # Barra de progresso para mostrar o progresso de alteração de permissões
                itens = [os.path.join(repos_dir, item) for item in os.listdir(repos_dir)]

                for item in tqdm(itens, desc=f"{' ' * 37}🛠️  Alterando permissões", unit=" passo"):
                    subprocess.run(f'icacls "{item}" /grant "{current_user}":F /T', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.run(f'attrib -R "{item}" /S /D', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                logging.info(f"🪟   Permissões alteradas com sucesso para \033[92m{repos_dir}\033[0m")

                # Depois de alterar as permissões, limpar o conteúdo da pasta
                logging.info(f"🗑️   Limpando o conteúdo da pasta de repositórios (\033[92m{repos_dir}\033[0m) antes do pipeline...")
                limpar_conteudo_pasta(repos_dir)

                print(" ")
                logging.info("\033[1m\033[93m✅   Conteúdo das pastas limpo com sucesso!\033[0m")
                print("=" * 120 + "\n")
        else:
            logging.info("\033[1m🚫   Limpeza não autorizada pelo usuário. Prosseguindo com o conteúdo atual das pastas...\033[0m]")
            print("=" * 120 + "\n")

        os.makedirs(data_path, exist_ok=True)
        os.makedirs(repos_dir, exist_ok=True)

        logging.info("🔄 Executando o pipeline completo...\n")
        buscar_repositorios()
        clone_repositories()
        coletar_dados()
        analisar_dados()
        logging.info("🎉 Pipeline finalizado com sucesso!")

    elif args.step == "buscar":
        buscar_repositorios()
    elif args.step == "clone":
        clone_repositories()
    elif args.step == "coletar":
        coletar_dados()
    elif args.step == "analisar":
        analisar_dados()

    logging.info("🎉 Pipeline finalizado com sucesso!")

if __name__ == "__main__":
    main()
