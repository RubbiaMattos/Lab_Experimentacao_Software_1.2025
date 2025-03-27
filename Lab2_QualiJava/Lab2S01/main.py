# 🚀 Instalando dependências essenciais...
import sys
import subprocess

# Lista de dependências externas
dependencias = [
    'os', 'csv', 'subprocess', 'logging', 'time', 'shutil', 'stat', 'psutil',
    'requests', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'statsmodels',
    'scipy', 'tabulate', 'datetime', 'python-dotenv', 'tqdm'
]

# Checagem e instalação das dependências (antes de carregar o logging)
print(f"\n{' ' * 37}🔎 Verificando e instalando dependências...\n")
for pacote in dependencias:
    try:
        __import__(pacote if pacote != 'python-dotenv' else 'dotenv')
        print(f"{' ' * 37}✅ {pacote.ljust(15)} -> Já instalado, pulando...")
    except ImportError:
        print(f"⬇️ {pacote.ljust(15)} -> ⏳ Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
        print(f"✅ {pacote.ljust(15)} -> 🎯 Instalada com sucesso!")

# ✅ Só agora importa as demais
import os
import logging
import argparse
import shutil
import time
import stat
from tqdm import tqdm

# Configura o logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
)

# AQUI SEGUE O TEU PIPELINE COMPLETO NORMAL
# Exemplo de etapa só pra manter o fluxo
print("\n")
logging.info("🎯 Ambiente pronto! Dependências verificadas e instaladas.")

print("\n" + "🟰" * 120)

BASE_DIR = os.path.dirname(__file__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
)

# Utilitários
def formatar_tempo(segundos):
    horas, resto = divmod(int(segundos), 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def run_subprocess(script_name):
    script_path = os.path.join(BASE_DIR, script_name)
    subprocess.run(["python", script_path], check=True)

# Etapas
def buscar_repositorios():
    logging.info("🌐 [ETAPA 1] BUSCAR REPOSITÓRIOS\n")
    start = time.time()
    run_subprocess('coleta_repositorios.py')
    end = time.time()
    logging.info(f"✅ Busca finalizada em {formatar_tempo(end - start)}")
    print("\n" + "🟰" * 120)

def clone_repositories():
    logging.info("🗂️ [ETAPA 2] CLONAR REPOSITÓRIOS\n")
    start = time.time()
    run_subprocess("automacao_clone.py")
    end = time.time()
    logging.info(f"✅ Clonagem finalizada em {formatar_tempo(end - start)}")
    print("\n" + "🟰" * 120)

def coletar_dados():
    logging.info("📊 [ETAPA 3] COLETAR DADOS\n")
    start = time.time()
    run_subprocess('coletar_dados.py')
    end = time.time()
    logging.info(f"✅ Coleta de dados finalizada em {formatar_tempo(end - start)}")
    print("\n" + "🟰" * 120)

def analisar_dados():
    logging.info("📈 [ETAPA 4] ANALISAR DADOS\n")
    start = time.time()
    run_subprocess('analisar_dados.py')
    end = time.time()
    logging.info(f"✅ Análise finalizada em {formatar_tempo(end - start)}")
    print("\n" + "🟰" * 120)

# Limpeza
def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def limpar_conteudo_pasta(pasta):
    if not os.path.exists(pasta):
        logging.warning(f"⚠️ Pasta {pasta} não encontrada para limpeza.")
        return
    itens = [item for item in os.listdir(pasta) if os.path.isdir(os.path.join(pasta, item))]
    if itens:
        with tqdm(total=len(itens), desc=f"{' ' * 37}🧹 Limpando {os.path.basename(pasta)}", unit=" pasta") as pbar:
            for item in itens:
                item_path = os.path.join(pasta, item)
                try:
                    shutil.rmtree(item_path, onerror=remove_readonly)
                    pbar.update(1)
                except Exception as e:
                    logging.warning(f"⚠️ Erro ao remover {item_path}: {e}")
    else:
        logging.info(f"📂 Pasta {os.path.basename(pasta)} está vazia.\n")

def limpeza_completa():
    data_path = os.path.join(BASE_DIR, "Data")
    repos_dir = os.path.join(BASE_DIR, "Repos")

    print(f"\n{' ' * 37}⚠️ Essa ação irá LIMPAR as pastas 'Data' e 'Repos'.")
    confirmacao = input(f"\n{' ' * 37}❓ Deseja continuar? (s/n): ").strip().lower()
    print("\n")

    if confirmacao == "s":
        if os.path.exists(data_path):
            logging.info(f"🪛 Limpando {os.path.basename(data_path)}")
            limpar_conteudo_pasta(data_path)

        if os.path.exists(repos_dir):
            logging.info(f"🪛 Limpando {os.path.basename(repos_dir)}")
            itens = [os.path.join(repos_dir, item) for item in os.listdir(repos_dir)]
            for item in tqdm(itens, desc=f"{' ' * 37}🔧 Permissões {os.path.basename(repos_dir)}", unit=" item"):
                try:
                    current_user = os.getlogin()
                except Exception:
                    import getpass
                    current_user = getpass.getuser()
                subprocess.run(f'icacls "{item}" /grant "{current_user}":F /T', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(f'attrib -R "{item}" /S /D', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            limpar_conteudo_pasta(repos_dir)

        logging.info("✅ Pastas limpas com sucesso!\n")
        print("\n" + "🟰" * 120)
    else:
        logging.info("🚫 Limpeza não autorizada. Prosseguindo sem limpar.\n")
        print("\n" + "🟰" * 120)

# MENU PRINCIPAL
def menu():
    while True:
        print(f"\n{' ' * 37}📌 MENU PRINCIPAL\n")
        print(f"{' ' * 37}1 - 🌐 BUSCAR REPOSITÓRIOS")
        print(f"{' ' * 37}2 - 🗂️ CLONAR REPOSITÓRIOS")
        print(f"{' ' * 37}3 - 📊 COLETAR DADOS")
        print(f"{' ' * 37}4 - 📈 ANALISAR DADOS")
        print(f"{' ' * 37}5 - 🔄 EXECUTAR PIPELINE COMPLETO")
        print(f"{' ' * 37}0 - 🚪 SAIR\n")


        escolha = input(f"\n{' ' * 37}🔎 Digite o número da opção desejada: ").strip()
        print("\n")

        if escolha == "1":
            buscar_repositorios()
            print("\n" + "🟰" * 120)
        elif escolha == "2":
            clone_repositories()
            print("\n" + "🟰" * 120)
        elif escolha == "3":
            coletar_dados()
            print("\n" + "🟰" * 120)
        elif escolha == "4":
            analisar_dados()
            print("\n" + "🟰" * 120)
        elif escolha == "5":
            logging.info("🔄 Executando PIPELINE COMPLETO 🔄\n")
            buscar_repositorios()
            clone_repositories()
            coletar_dados()
            analisar_dados()
            logging.info("🎉 Pipeline finalizado com sucesso!")
            print("\n" + "🟰" * 120)
            break
        elif escolha == "0":
            logging.info("🚪 Encerrando o programa.\n")
            break
        else:
            logging.warning("🚫 Opção inválida.\n")

if __name__ == "__main__":
    # Sempre executa a limpeza antes de abrir o menu
    limpeza_completa()
    menu()
