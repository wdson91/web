from imports import *
from vmz.vmzdisney.vmz_disney import coletar_precos_vmz_disneybasicos, coletar_precos_vmz_disneydias

from .voupradisney.voupradisney import coletar_precos_voupra_disney
from .vouprasea.vouprasea import coletar_precos_voupra_sea
from .vouprauniversal.vouprauniversal import coletar_precos_voupra_universal

nome_pacotes = {
        2: "2 Dias - Disney World Basico",
        3: "3 Dias - Disney World Basico",
        4: "4 Dias - Disney World Basico",
        5: "5 Dias - Disney World Basico"
    }
async def main_voupra(hour,array_datas,run_once=False):
    if run_once:
        logging.info("Iniciando coleta de preços.")
        try:
            await asyncio.gather(
                coletar_precos_vmz_disneydias(nome_pacotes,array_datas, hour),
                coletar_precos_voupra_disney(hour, array_datas),
                coletar_precos_vmz_disneybasicos(array_datas,hour),
                coletar_precos_voupra_universal(hour, array_datas),
                coletar_precos_voupra_sea(hour, array_datas)
            )
        except Exception as e:
        
            logging.error(f"Erro ao coletar preços: {e}")
            
        return 
    
if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_voupra())
