import os
import logging
import sys
from dotenv import load_dotenv
from typing import Optional

# Caminho baseado no diretório da sprint
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, ".."))
log_dir = os.path.join(base_dir, "Relatórios")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "config_token.log")

# Configuração do logging (console + arquivo)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file, encoding="utf-8")
    ]
)
log = logging.getLogger(__name__)

def configurar_token(
    nome_variavel: str = "GITHUB_TOKEN",
    caminho_env: Optional[str] = None
) -> str:
    if caminho_env is None:
        caminho_env = os.path.abspath(os.path.join(script_dir, "env.config"))

    if os.path.exists(caminho_env):
        load_dotenv(dotenv_path=caminho_env)
        print("\n")
        log.info(f"✅ Arquivo de ambiente carregado: {os.path.relpath(caminho_env)}")
    else:
        raise FileNotFoundError(f"❌ ERRO: Arquivo env.config não encontrado: {caminho_env}")

    token = os.getenv(nome_variavel)
    if not token:
        raise ValueError(f"❌ ERRO: Variável '{nome_variavel}' não foi encontrada no arquivo {caminho_env} 🔐")

    log.info(f"✅ Token '{nome_variavel}' carregado com sucesso.\n")
    return token
