import asyncio
import logging
from ml.index_ml import main_ml
from voupra.index_voupra import main_voupra # Importando a função main do primeiro script
from vmz.index_vmz import main_vmz # Importando a função do segundo script
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
async def executar_ambos():
   while True:  # Adicionando um loop para continuar executando
        await asyncio.gather(
            main_vmz(run_once=True),
            main_voupra(run_once=True),
            main_ml(run_once=True)
        )
        logging.info("Aguardando a próxima execução...")
        await asyncio.sleep(1200)  # Aguarda por 1 hora

if __name__ == "__main__":
    asyncio.run(executar_ambos())