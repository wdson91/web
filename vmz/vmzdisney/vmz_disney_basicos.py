import asyncio
import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
import logging

diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível

# Adicionando o diretório 'docs' ao sys.path
sys.path.insert(0, diretorio_avo)
from salvardados import salvar_dados
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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Definindo as datas
    datas = [datetime.now().date() + timedelta(days=d) for d in [5, 10, 20, 47, 64, 126]]

    # Lista para armazenar os dados
    dados = []

    # Lista de parques e XPaths na sequência desejada
    parques_xpaths = [
        ("1 Dia - Disney Básico Magic Kingdom", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b'),
        ("1 Dia - Disney Básico Hollywood Studios", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b'),
        ("1 Dia - Disney Básico Animal Kingdom", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b'),
        ("1 Dia - Disney Básico Epcot", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b'),
        ("4 Dias - Disney Promocional",'//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[3]/div[1]/b')
    ]

    # Criar um dicionário para mapear os nomes dos parques para os URLs correspondentes
    parque_url_map = {parque: url for url, xpath, parque in sites}

    for data in datas:
        logging.info(f"Coletando preços para a data: {data}")
        for parque, xpath_selector in parques_xpaths:
            
            logging.info(f"Acessando {parque}...")
            site_url = parque_url_map.get(parque, '')
            if site_url:
                url = f"{site_url}data={data.strftime('%Y-%m-%d')}"
                driver.get(url)

                try:
                    # Tente localizar o elemento com o preço
                    wait = WebDriverWait(driver, 10)
                    elemento_preco = driver.find_element(By.XPATH, xpath_selector)
                    preco_texto = elemento_preco.text
                    

                    # Multiplicar o preço por 10
                    preco_texto = preco_texto.replace('R$ ', '').replace(',', '.')
                    preco_float = float(preco_texto) * 10
                    preco_texto = f"R$ {preco_float:.2f}"
                except NoSuchElementException:
                    

                    # Se o elemento não for encontrado, atribua um traço "-" ao valor
                    preco_texto = "-"

                # Adicione os dados a lista de dicionários
                dados.append({'Data_Hora_Coleta': datetime.now(), 'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"), 'Parque': parque, 'Preco': preco_texto})
    logging.info("Coleta finalizada.")
    # Fechando o driver
    driver.quit()

    # Criando um DataFrame
    df = pd.DataFrame(dados)

    salvar_dados(df, diretorio_atual, 'vmz_disney_basicos')

    logging.info("Coleta finalizada Site Vmz- Disney.")
    
if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_disneybasicos())