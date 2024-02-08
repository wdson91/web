import asyncio
import os
import sys
import time
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import logging


async def coletar_precos_vmz_disneybasicos():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Lista de sites, XPaths e nomes de parques
    sites = [
        ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-magic-kingdom-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Magic Kingdom'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/epcot?",  '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Epcot'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-hollywood-studios-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Hollywood Studios'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-animal-kingdom-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Animal Kingdom'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/promocao-disney-world-4-park-magic/promocao-disney-world-4-park-magic?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[3]/div[1]/b', '4 Dias - Disney Promocional')
        # Adicione outros sites, XPaths e nomes de parques conforme necessário
    ]

    # Configuração inicial do Selenium
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)

    # Definindo as datas
    datas = [datetime.now().date() + timedelta(days=d) for d in [5, 10, 20, 47, 64, 126]]

    # Lista para armazenar os dados
    dados = []

    for data in datas:
        logging.info(f"Coletando preços para a data: {data}")
        for site_url, xpath_selector, parque in sites:
            
            logging.info(f"Acessando {parque}...")
            url = f"{site_url}data={data.strftime('%Y-%m-%d')}"
            driver.get(url)

            try:
                # Tente localizar o elemento com o preço
                wait = WebDriverWait(driver, 10)
                elemento_preco = wait.until(EC.presence_of_element_located((By.XPATH, xpath_selector)))
                
                # Obtenha o texto do elemento usando get_attribute("innerText")
                preco_texto = elemento_preco.get_attribute("innerText")

                # Multiplicar o preço por 10
                price_decimal = float(preco_texto.replace('R$', '').replace('.', '').replace(',', '.').strip())
                new_price = round(price_decimal * 1.10, 2)
                new_price *= 10
                new_price = round(new_price, 2)
            except NoSuchElementException:
                # Se o elemento não for encontrado, atribua um traço "-" ao valor
                new_price = "-"

            data_hora_atual = datetime.now()
            dados.append({
                'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"),
                'Parque': parque,
                'Preco': new_price
            })
            print(dados)
    logging.info("Coleta finalizada.")
    # Fechando o driver
    driver.quit()

    # Criando um DataFrame
    df = pd.DataFrame(dados)
    print(df)
    
    #inserir_dados_no_banco(df, 'vmz_disney')
    nome_arquivo = f'{datetime.now().strftime("%Y-%m-%d")}_vmz_disney.json'
    #salvar_dados(df, nome_arquivo,'vmz')
    logging.info("Coleta finalizada Site Vmz- Disney.")
    
if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_disneybasicos())
