import os 
import logging 
from dotenv import load_dotenv 
from typing import List ,Optional 
from github import Github 
from datetime import datetime ,timezone 

os .environ ['PYTHONDONTWRITEBYTECODE']='1'

script_dir =os .path .dirname (os .path .abspath (__file__ ))

def setup_logger (name :str ,level :int =logging .INFO )->logging .Logger :
    """Configura o logger com o nível especificado."""
    logger =logging .getLogger (name )
    handler =logging .StreamHandler ()
    formatter =logging .Formatter ('%(asctime)s - %(levelname)s - %(message)s')
    handler .setFormatter (formatter )
    logger .addHandler (handler )
    logger .setLevel (level )
    return logger 

logger =setup_logger (__name__ )

def format_duration (seconds :float )->str :
    """Converte segundos em string HH:MM:SS."""
    seconds =max (0 ,int (seconds ))
    h =seconds //3600 
    m =(seconds %3600 )//60 
    s =seconds %60 
    return f"{h :02d}:{m :02d}:{s :02d}"

def configurar_token (
prefix :str ="GITHUB_TOKEN",
caminho_env :Optional [str ]=None ,
log_ambiente :bool =True ,
log_level :int =logging .INFO 
)->List [str ]:
    """
    Carrega um ou mais tokens a partir de um arquivo de configuração .env e exibe status de rate-limit.

    :param prefix: Prefixo das variáveis de ambiente (ex: "GITHUB_TOKEN" ou "GITHUB_TOKEN_1").
    :param caminho_env: Caminho para o arquivo .env (se None, usa 'env.config' no mesmo diretório).
    :param log_ambiente: Se True, exibe logs informativos.
    :param log_level: Nível do log (DEBUG, INFO, ERROR).
    :return: Lista de tokens encontrados.
    """
    logger .setLevel (log_level )


    if caminho_env is None :
        caminho_env =os .path .abspath (os .path .join (script_dir ,"env.config"))


    if os .path .exists (caminho_env ):
        load_dotenv (dotenv_path =caminho_env )
        if log_ambiente :
            print (f"🔄 Arquivo de ambiente carregado: {os .path .relpath (caminho_env )}")
    else :
        raise FileNotFoundError (f"❌ ERRO: Arquivo env.config não encontrado: {caminho_env }")


    tokens :List [str ]=[]
    var_names :List [str ]=[]


    token_base =os .getenv (prefix )
    if token_base :
        tokens .append (token_base )
        var_names .append (prefix )

    idx =1 
    while True :
        name =f"{prefix }_{idx }"
        value =os .getenv (name )
        if not value :
            break 
        tokens .append (value )
        var_names .append (name )
        idx +=1 

    if not tokens :
        raise ValueError (f"❌ ERRO: Nenhum token encontrado para prefixo '{prefix }' em {caminho_env }")

    if log_ambiente :

        print (f"🔑 Tokens carregados ({len (tokens )}):")
        for name ,token in zip (var_names ,tokens ):
            gh =Github (token )
            core =gh .get_rate_limit ().core 
            now =datetime .now (timezone .utc )
            wait =(core .reset -now ).total_seconds ()
            print (f"    🔒 {name } →")
            print (f"        💚 Limite restante:  {core .remaining }")
            print (f"        ⏰ Próximo reset em: {format_duration (wait )}\n")
        print ()

    return tokens 
