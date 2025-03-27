import os
import logging
from dotenv import load_dotenv
from typing import Optional

# Diretório base para logs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "Relatórios")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "config_token.log")

# Configuração do logging (console + arquivo)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)
log = logging.getLogger(__name__)

def configurar_token(
    nome_variavel: str = "GITHUB_TOKEN",
    caminho_env: Optional[str] = None
) -> str:
    """
    Carrega um token de API de um arquivo .env/config.

    Args:
        nome_variavel (str): Nome da variável de ambiente a ser lida.
        caminho_env (str, opcional):Caminho completo para o arquivo .env/config.
                                    Se None, assume caminho relativo ao script.

    Returns:
        str: Token recuperado da variável de ambiente.

    Raises:
        FileNotFoundError: Se o arquivo .env/config não for encontrado.
        ValueError: Se a variável não estiver definida no arquivo.
    """
    if caminho_env is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_env = os.path.abspath(os.path.join(script_dir, "..", "..", "env.config"))

    if os.path.exists(caminho_env):
        load_dotenv(dotenv_path=caminho_env)
        log.info(f"✅ Arquivo de ambiente carregado: {caminho_env}")
    else:
        raise FileNotFoundError(f"❌ ERRO: Arquivo env.config não encontrado: {caminho_env}")

    token = os.getenv(nome_variavel)
    if not token:
        raise ValueError(f"❌ ERRO: Variável '{nome_variavel}' não foi encontrada no arquivo {caminho_env} 🔐")

    log.info(f"✅ Token '{nome_variavel}' carregado com sucesso.")
    return token
