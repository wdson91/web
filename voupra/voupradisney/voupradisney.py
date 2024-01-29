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

diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível

# Adicionando o diretório 'docs' ao sys.path
sys.path.insert(0, diretorio_avo)
from salvardados import salvar_dados

async def coletar_precos_voupra_disney():
    # Configuração inicial do Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Configuração de logs
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    # Definindo as datas de viagem
    datas_viagem = [datetime.now().date() + timedelta(days=d) for d in [5]]

    # Definindo os nomes dos parques e os XPaths correspondentes
    parques_xpaths = [
        ("1 Dia - Disney Basico Magic Kingdom", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[4]/div/div/div[3]/div[1]/div[2]'),
        ("1 Dia - Disney Basico Hollywood Studios", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[12]/div/div/div[3]/div[1]/div[2]'),
        ("1 Dia - Disney Basico Animal Kingdom", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[19]/div/div/div[3]/div[1]/div[2]'),
        ("1 Dia - Disney Basico Epcot", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[27]/div/div/div[3]/div[1]/div[2]'),
        ("2 Dias - Disney World Bsico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[34]/div/div/div[3]/div[1]/div[2]'),
        ("3 Dias - Disney World Basico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[42]/div/div/div[3]/div[1]/div[2]'),
        ("4 Dias - Disney World Basico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[56]/div/div/div[3]/div[1]/div[2]'),
        ("4 Dias - Disney Promocional", '//*[@id="id-59523"]/div/div/div[3]/div[1]/div[2]'),
        ("5 Dias - Disney World Basico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[63]/div/div/div[3]/div[1]/div[2]'),
    ]
    
    # Lista para armazenar os dados
    dados = []

    # Iniciar o log
    logging.info("Iniciando a coleta de preços de ingressos da Disney no site Voupra.")

    for data_viagem in datas_viagem:
        for parque, xpath in parques_xpaths:
            url = f"https://www.voupra.com/estados-unidos/orlando/disney-world?Id=49824&DataIngresso={data_viagem.strftime('%d%%2F%m%%2F%Y')}"
            driver.get(url)

            try:
                if parque == "4 Dias - Disney Promocional":
                    # Check if the element //*[@id="id-59523"] is present
                    try:
                        driver.find_element(By.XPATH, '//*[@id="id-59523"]')
                        # The element is present, get the price from the corresponding XPath
                        elemento_preco = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[49]/div/div/div[3]/div[1]/div[2]')
                    except NoSuchElementException:
                        # The element is not present, set the price to "-"
                        preco_texto = "-"
                else:
                    # For other parks, get the price directly
                    elemento_preco = driver.find_element(By.XPATH, xpath)
                    preco_texto = elemento_preco.text
            except TimeoutException:
                # Handle the timeout exception here
                preco_texto = "-"


            # Adicione os dados a lista de dicionários
            dados.append({
                'Data_Hora_Coleta': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                'Data_viagem': data_viagem.strftime('%Y-%m-%d'),
                'Parque': parque,
                'Preco': preco_texto
            })

    # Fechando o driver
    driver.quit()
    
    # Criando um DataFrame
    df = pd.DataFrame(dados)

    
    salvar_dados(df, diretorio_atual, 'voupra_disney')
    
    logging.info("Coleta finalizada Site Voupra - Disney.")



if __name__ == '__main__':
    asyncio.run(coletar_precos_voupra_disney())
