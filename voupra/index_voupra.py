from imports import *

from .voupradisney.voupradisney import coletar_precos_voupra_disney
from .vouprasea.vouprasea import coletar_precos_voupra_sea
from .vouprauniversal.vouprauniversal import coletar_precos_voupra_universal


async def main_voupra(run_once=False):
    if run_once:
        logging.info("Iniciando coleta de preços.")
        try:
            # Execute as funções assíncronas em sequência
            #await coletar_precos_voupra_disney()
            await coletar_precos_voupra_sea()
            #await coletar_precos_voupra_universal()
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços: {e}")

        return 
    
if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_voupra())
