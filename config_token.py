import os
import logging
from dotenv import load_dotenv
from typing import Optional

# Impede a criação do __pycache__
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Caminho baseado no diretório da sprint
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, ".."))

# Configuração do logger com nível ajustável
def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """ Configura o logger com o nível especificado. """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger

# Inicializar o logger
logger = setup_logger(__name__)

def configurar_token(
    nome_variavel: str = "GITHUB_TOKEN",
    caminho_env: Optional[str] = None,
    log_ambiente: bool = True,  # Controla as mensagens de log
    log_level: int = logging.INFO  # Controla o nível do log (INFO, DEBUG, ERROR)
) -> str:
    """
    Carrega o token a partir de um arquivo de configuração .env e retorna seu valor.

    :param nome_variavel: Nome da variável de ambiente a ser carregada.
    :param caminho_env: Caminho para o arquivo .env (se None, usa 'env.config' no diretório atual).
    :param log_ambiente: Se True, exibe logs informativos sobre o carregamento.
    :param log_level: Nível do log (ex: logging.DEBUG, logging.INFO).
    :return: O valor do token.
    """
    # Configurar o logger com o nível apropriado
    logger.setLevel(log_level)

    if caminho_env is None:
        caminho_env = os.path.abspath(os.path.join(script_dir, "env.config"))

    # Verifica se o arquivo .env existe
    if os.path.exists(caminho_env):
        load_dotenv(dotenv_path=caminho_env)

        if log_ambiente:
            print(f"✅ Arquivo de ambiente carregado: {os.path.relpath(caminho_env)}")
    else:
        print(f"❌ ERRO: Arquivo env.config não encontrado: {caminho_env}")
        raise FileNotFoundError(f"❌ ERRO: Arquivo env.config não encontrado: {caminho_env}")

    # Obtém o token a partir da variável de ambiente
    token = os.getenv(nome_variavel)
    
    # Verifica se o token foi encontrado
    if not token:
        print(f"❌ ERRO: Variável '{nome_variavel}' não foi encontrada no arquivo {caminho_env} 🔐")
        raise ValueError(f"❌ ERRO: Variável '{nome_variavel}' não foi encontrada no arquivo {caminho_env} 🔐")
    
    if log_ambiente:
        print(f"✅ Token '{nome_variavel}' carregado com sucesso.\n")

    return token
