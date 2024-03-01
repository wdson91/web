from imports import *

from .vmzdisney.vmz_disney import coletar_precos_vmz
from .vmzsea.vmzsea import coletar_precos_vmz_seaworld
from .vmzuniversal.vmzuniversal import coletar_precos_vmz_universal


async def main_vmz(hour,array_datas,run_once=False):
    if run_once:
        logging.info("Iniciando coleta de preços.")
        try:
            await asyncio.gather(
                coletar_precos_vmz(hour,array_datas),
                coletar_precos_vmz_seaworld(hour,array_datas),
                coletar_precos_vmz_universal(hour, array_datas)
            )
            # Execute as funções assíncronas em sequência
           
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")
            
        return


if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_vmz())
