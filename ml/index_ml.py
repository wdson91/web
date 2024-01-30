import asyncio
import sys
import os
import logging

from ml.ml_universal.ml_universal import coletar_precos_ml_universal
from ml.mldisney.ml_disney import coletar_precos_ml_disney
from ml.mlsea.mlsea import coletar_precos_ml_seaworld



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        # # Aguarda por 1 hora (3600 segundos)
        # logging.info("Aguardando a próxima execução...")
        # await asyncio.sleep(3600)  # 3600 segundos = 1 hora

if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_ml())
