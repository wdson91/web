import asyncio
import logging
from ml.index_ml import main_ml
from voupra.index_voupra import main_voupra # Importando a função main do primeiro script
from vmz.index_vmz import main_vmz # Importando a função do segundo script

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def executar_ambos():
    # Executando ambas as funções assíncronas simultaneamente
    await asyncio.gather(
        
        main_vmz(run_once=True),
        main_voupra(run_once=True),
        main_ml(run_once=True)
    )

     # # Aguarda por 1 hora (3600 segundos)
    logging.info("Aguardando a próxima execução...")
    await asyncio.sleep(3600)  # 3600 segundos = 1 hora

if __name__ == "__main__":
    asyncio.run(executar_ambos())
