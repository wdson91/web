from imports import *

from .vmzdisney.vmz_disney import coletar_precos_vmz_disney
from .vmzsea.vmzsea import coletar_precos_vmz_seaworld
from .vmzuniversal.vmzuniversal import coletar_precos_vmz_universal

async def main_vmz(run_once=False):
    if run_once:
        logging.info("Iniciando coleta de preços.")
        try:
            # Execute as funções assíncronas em sequência
            await coletar_precos_vmz_disney()
            await coletar_precos_vmz_seaworld()
            await coletar_precos_vmz_universal()
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços: {e}")

        return
        # # Aguarda por 1 hora (3600 segundos)
        # logging.info("Aguardando a próxima execução...")
        # await asyncio.sleep(3600)  # 3600 segundos = 1 hora

if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_vmz())
