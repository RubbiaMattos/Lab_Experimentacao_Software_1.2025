import subprocess
import sys
import importlib.metadata
from datetime import datetime

start_time = datetime.now()
print(f"🕒 Início da execução: {start_time.strftime('%d/%m/%Y %H:%M:%S')}")

# Lista de dependências essenciais para o projeto
dependencias = [
    # 📦 Essenciais para o projeto
    'requests',          # Requisições HTTP (GraphQL, REST)
    'pandas',            # Manipulação de CSV/DataFrame
    'numpy',             # Cálculos numéricos
    'scipy',             # Correlações estatísticas
    'tqdm',              # Barras de progresso
    'PyGithub',          # Integração com GitHub API
    'openpyxl',          # Exportação para Excel
    'matplotlib',        # Visualização gráfica
    'seaborn',           # Visualização estatística
    'plotly',            # Visualizações interativas

    # 🧰 Opcionais úteis e estilização
    'tabulate',          # Tabelas no terminal
    'rich',              # Output bonito e colorido no terminal
    'typer',             # Criação de CLI elegante
    'python-dotenv',     # Variáveis de ambiente (.env)
]

print("\n🔍 Verificando e instalando dependências...")

def check_and_install(package):
    print(f"\n🔧 Verificando e instalando a dependência: {package}")

    try:
        # Verificar se o pacote já está instalado
        
        installed_version = importlib.metadata.version(package)
        print(f"    🎯 {package} (v{installed_version}) já está instalado.")
        
        # Obter a versão mais recente disponível do pacote
        print(f"        🔍 Verificando se {package} precisa ser atualizado...")
        result = subprocess.run([sys.executable, "-m", "pip", "show", package], capture_output=True, text=True)
        latest_version = result.stdout.splitlines()[1].split(":")[1].strip()

        # Comparar a versão instalada com a versão mais recente
        if installed_version == latest_version:
            print(f"        👍 {package} está na versão mais recente.")
        else:
            print(f"        🔄 {package} precisa ser atualizado. Atualizando para v{latest_version}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
            print(f"        🚀 {package} foi atualizado para a versão mais recente. 🎉")
    
    except importlib.metadata.PackageNotFoundError:
        # Caso o pacote não esteja instalado, ele será instalado
        print(f"        ⬇️ {package} não encontrado. Instalando... 🔧")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Atualizar ou instalar pacotes conforme necessário
for pacote in dependencias:
    check_and_install(pacote)

import os
import time
import logging

# Configuração do logging (console + arquivo)
script_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(script_dir)

# Configuração do log
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

print("\n🎯 Ambiente pronto! Dependências verificadas e instaladas.")

print("\n" + "-" * 120 + "\n")

# ⏱️ Utilitário de formatação de tempo
def formatar_tempo(segundos):
    
    minutos, segundos = divmod(int(segundos), 60)
    horas, minutos = divmod(minutos, 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

# 🧠 Executa subprocesso
def run_subprocess(script_name):
    
    path = os.path.join(script_dir, script_name)
    subprocess.run([sys.executable, path], check=True)

def collect_repos():
    
    print("\n🌐 [ETAPA 1] BUSCAR REPOSITÓRIOS\n")
    start = time.time()
    run_subprocess('collect_repos.py')
    end = time.time()
    tempo = formatar_tempo(end - start)
    print(f"✅ Busca finalizada em {tempo}")
    print("\n" + "-" * 120)

def collect_prs():
    
    print("\n🔧 [ETAPA 2] COLETAR PULL REQUESTS\n")
    start = time.time()
    run_subprocess("collect_prs.py")
    end = time.time()
    tempo = formatar_tempo(end - start)
    print(f"✅ Coleta de PRs finalizada em {tempo}")
    print("\n" + "-" * 120)

def analyze_data():
    
    print("\n📊 [ETAPA 3] ANALISAR DADOS\n")
    start = time.time()
    run_subprocess('analyze_data.py')
    end = time.time()
    tempo = formatar_tempo(end - start)
    print(f"✅ Análise finalizada em {tempo}")
    print("\n" + "-" * 120)

# MENU PRINCIPAL
def menu():
    
    while True:
        print(f"📌 MENU PRINCIPAL\n")
        print(f"    1  - 🌐 Buscar repositórios")
        print(f"    2  - 🔧 Coletar pull requests")
        print(f"    3  - 📊 Analisar dados")
        print(f"    4  - 🔄 Executar pipeline completo")
        print(f"    0  - 🚪 Sair")

        escolha = input(f"\n👉 Digite sua opção: ").strip()
        print("\n" + "-" * 120)

        if escolha == "1":
            collect_repos()
            print("\n" + "-" * 120)
        elif escolha == "2":
            collect_prs()
            print("\n" + "-" * 120)
        elif escolha == "3":
            analyze_data()
            print("\n" + "-" * 120)
        elif escolha == "4":
            print("\n🔄 Executando PIPELINE COMPLETO 🔄")
            inicio_total = time.time()

            collect_repos()
            collect_prs()
            analyze_data()

            fim_total = time.time()
            tempo_total = formatar_tempo(fim_total - inicio_total)

            print(f"\n🎉 Pipeline finalizado com sucesso!")
            print(f"⏱️ Tempo total de execução do pipeline: {tempo_total}")
            print("\n" + "-" * 120)
            break
        elif escolha == "0":
            print("\n👋 Encerrando o pipeline. Até breve!")
            print("\n" + "-" * 120)
            break
        else:
            print("🚫 Opção inválida.")
            print("\n" + "-" * 120)
            
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"\n🕔 Fim da execução: {end_time.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"⏱️ Duração total: {str(duration)}\n")

if __name__ == "__main__":
    menu()
