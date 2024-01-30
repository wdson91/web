import asyncio
import os
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
import logging
from insert_database import inserir_dados_no_banco
# Configuração inicial do Selenium


diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível
sys.path.insert(0, diretorio_avo)
from salvardados import salvar_dados

async def coletar_precos_voupra_sea():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)
    # Definindo as datas de viagem
    datas = [datetime.now().date() + timedelta(days=d) for d in [5, 10, 20, 47, 64, 126]]

    # Definindo os nomes dos parques e os XPaths correspondentes
    parques_xpaths = [
        ("1 Dia 1 Parque - SeaWorld Orlando", '/html/body/div[4]/div/div[1]/div[2]/div[12]/div/div/div[3]/div[1]/div[2]'),
        ("3 Dias 3 Parques - SeaWorld Orlando", '/html/body/div[4]/div/div[1]/div[2]/div[6]/div/div/div[3]/div[1]/div[2]'),
        ("14 Dias 3 Parques - SeaWorld Orlando", '/html/body/div[4]/div/div[1]/div[2]/div[27]/div/div/div[3]/div[1]/div[2]')
    ]


    # Lista para armazenar os dados
    dados = []
    logging.info("Iniciando a coleta de precos de ingressos Seaworld no site Voupra.")
    for data in datas:
        for parque, xpath in parques_xpaths:
            url = f"https://www.voupra.com/estados-unidos/orlando/seaworld?Id=58825&Busca=true&DataTemporada={data.strftime('%d%%2F%m%%2F%Y')}"
            driver.get(url)

            try:
                # Tente localizar o elemento com o preço
                wait = WebDriverWait(driver, 10)
                elemento_preco = driver.find_element(By.XPATH, xpath)
                preco_texto = elemento_preco.text
                preco_final = float(preco_texto.replace('R$', '').replace('.', '').replace(',', '.').strip())
                
            except NoSuchElementException:
                # Se o elemento não for encontrado, atribua um traço "-" ao valor
                preco_final = "-"

            # Adicione os dados a lista de dicionários
            data_hora_atual = datetime.now()
            dados.append({
                    'Data_Coleta': data_hora_atual.strftime("%Y-%m-%d"),
                    'Hora_Coleta': data_hora_atual.strftime("%H:%M:%S"),
                    'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"),
                    'Parque': parque,
                    'Preco': preco_final
                })    
            
    # Fechando o driver
    driver.quit()

    # Criando um DataFrame
    df = pd.DataFrame(dados)
    

    # Inserindo os dados no banco de dados
    inserir_dados_no_banco(df, 'voupra_seaworld')    
    
    
    logging.info("Coleta finalizada.")
    # Salvando em um arquivo TXT

if __name__ == '__main__':
    asyncio.run(coletar_precos_voupra_sea())