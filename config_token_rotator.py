from github import Github 
from datetime import datetime ,timezone 
import time 

class TokenRotator :
    """
    Gerencia múltiplos tokens do GitHub e alterna automaticamente quando um token está baixo.

    :param tokens: lista de Personal Access Tokens.
    :param threshold: chamadas mínimas antes de trocar de token.
    :param low_wait: espera, em segundos, quando usar token abaixo do threshold.
    """
    def __init__ (self ,tokens :list [str ],threshold :int =100 ,low_wait :int =60 ):
        if not tokens :
            raise ValueError ("Lista de tokens não pode estar vazia.")
        self .tokens =tokens 
        self .threshold =threshold 
        self .low_wait =low_wait 

        self .clients =[Github (t )for t in tokens ]
        self .idx =0 

    def switch (self ):
        """
        Alterna manualmente para o próximo token.
        """
        self .idx =(self .idx +1 )%len (self .clients )
        print (f"🔄 Switch manual para token #{self .idx +1 }")

    def get (self )->Github :
        """
        Retorna um cliente válido:
        - se current.remaining > threshold, usa mesmo token;
        - senão, busca próximo > threshold;
        - senão, busca qualquer >0 (com um delay low_wait);
        - se todos zerados, aguarda reset e retorna current.
        """
        now =datetime .now (timezone .utc )

        client =self .clients [self .idx ]
        core =client .get_rate_limit ().core 
        if core .remaining >self .threshold :
            return client 

        for _ in range (1 ,len (self .clients )):
            self .idx =(self .idx +1 )%len (self .clients )
            client =self .clients [self .idx ]
            core =client .get_rate_limit ().core 
            if core .remaining >self .threshold :
                print (f"🔄 Threshold atingido, token #{self .idx +1 } com remaining={core .remaining }")
                return client 

        for _ in range (len (self .clients )):
            client =self .clients [self .idx ]
            core =client .get_rate_limit ().core 
            if core .remaining >0 :
                print (f"⚠️ Token #{self .idx +1 } com remaining baixo ({core .remaining }), aguardando {self .low_wait }s")
                time .sleep (self .low_wait )
                return client 
            self .idx =(self .idx +1 )%len (self .clients )

        resets =[c .get_rate_limit ().core .reset for c in self .clients ]
        earliest =min (resets )
        wait =max ((earliest -now ).total_seconds ()+5 ,0 )
        reset_str =earliest .astimezone (timezone ).strftime ('%d/%m/%Y %H:%M:%S')
        print (f"⏳ Todos tokens zerados, aguardando {int (wait )}s até reset ({reset_str })")
        time .sleep (wait )

        client =self .clients [self .idx ]
        return client 

    def get_token (self )->str :
        """Retorna o token atual como string (útil para chamadas REST diretas)."""
        return self .tokens [self .idx ]
