import asyncio
import logging
from voupra.index_voupra import main_voupra # Importando a função main do primeiro script
from vmz.index_vmz import main_vmz # Importando a função do segundo script

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def executar_ambos():
    # Executando ambas as funções assíncronas simultaneamente
    await asyncio.gather(
        
        main_vmz(run_once=True),
        main_voupra(run_once=True)
    )

if __name__ == "__main__":
    asyncio.run(executar_ambos())
