import asyncio
import pandas as pd
import logging
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import os
import sys
import time

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_pai = os.path.dirname(diretorio_atual)
diretorio_avo = os.path.dirname(diretorio_pai)

sys.path.insert(0, diretorio_avo)
from salvardados import salvar_dados

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

async def scroll_ate_elemento(driver, elemento):
    driver.execute_script("arguments[0].scrollIntoView();", elemento)

async def coletar_precos_decolar_disney():
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    urls_xpaths_parques_decolar_disney = [
        ("https://www.decolar.com/atracoes-turisticas/d-DY_ORL/ingressos+para+walt+disney+world+resort-orlando?from=2024-01-25&to=2025-01-25&destination=ORL&distribution=1&fixedDate=2024-01-30&modalityId=ANNUAL-MK-2024", '/html/body/app-root/detail-general/div/div/ticket-modalities/div/div/div/div/div/div/div[1]/div[11]/ticket-modality-cluster/div/ticket-cluster-prices/ul/li[1]/span[2]', "1 Dia - Disney Básico Magic Kingdom - 2024"),
        ("https://www.decolar.com/atracoes-turisticas/d-DY_ORL/ingressos+para+walt+disney+world+resort-orlando?from=2024-01-25&to=2025-01-25&destination=ORL&distribution=1&fixedDate=2024-01-30&modalityId=ANNUAL-MK-2024", '/html/body/app-root/detail-general/div/div/ticket-modalities/div/div/div/div/div/div/div[1]/div[14]/ticket-modality-cluster/div/ticket-cluster-prices/ul/li[1]/span[2]', "1 Dia - Disney Básico Hollywood Studios"),
        # Adicione os outros parques aqui com os respectivos URLs e XPaths
    ]
    
    datas = [datetime.now().date() + timedelta(days=d) for d in [5, 10, 20, 47, 64, 126]]
    dados = []

    logging.info("Iniciando a coleta de preços de ingressos da Disney no site Decolar.")

    for url, xpath, nome_parque in urls_xpaths_parques_decolar_disney:
        for data in datas:
            url_com_data = f"{url}&from={data}&to={data}"
            driver.get(url_com_data)

            # Aguarde 5 segundos
            time.sleep(10)

            try:
                # Aguarde até que o elemento seja visível
                elemento_preco = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))

                # Role até o elemento desejado
                #await scroll_ate_elemento(driver, elemento_preco)

                # Aguarde mais 10 segundos
                time.sleep(10)

                preco_texto = elemento_preco.text
            except TimeoutException:
                preco_texto = "-"

            data_hora_atual = datetime.now()
            dados.append({
                'Data_Coleta': data_hora_atual.strftime("%Y-%m-%d"),
                'Hora_Coleta': data_hora_atual.strftime("%H:%M:%S"),
                'Data_viagem': data.strftime("%Y-%m-%d"),
                'Parque': nome_parque,
                'Preco': preco_texto
            })

    driver.quit()

    df = pd.DataFrame(dados)
    
    print(df)

    logging.info("Coleta finalizada no site Decolar - Disney.")

if __name__ == '__main__':
    asyncio.run(coletar_precos_decolar_disney())
 