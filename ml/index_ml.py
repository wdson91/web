from imports import *

from ml.ml_universal.ml_universal import coletar_precos_ml_universal
from ml.mldisney.ml_disney import coletar_precos_ml_disney
from ml.mlsea.mlsea import coletar_precos_ml_seaworld




async def main_ml(run_once=False):
    if run_once:
        logging.info("Iniciando coleta de preços.")
        try:
            
            # Execute as funções assíncronas em sequência
            await coletar_precos_ml_disney()
            await coletar_precos_ml_seaworld()
            await coletar_precos_ml_universal()
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços: {e}")

        return 
if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_ml())
