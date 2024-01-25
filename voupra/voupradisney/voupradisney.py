import asyncio
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import os


async def coletar_precos_voupra_disney():
    # Configuração inicial do Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Configuração de logs
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    # Definindo as datas de viagem
    datas_viagem = [datetime.now().date() + timedelta(days=d) for d in [5, 10, 20, 47, 64, 126]]

    # Definindo os nomes dos parques e os XPaths correspondentes
    parques_xpaths = [
        ("1 Dia - Disney Basico Magic Kingdom", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[4]/div/div/div[3]/div[1]/div[2]'),
        ("1 Dia - Disney Basico Hollywood Studios", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[12]/div/div/div[3]/div[1]/div[2]'),
        ("1 Dia - Disney Basico Animal Kingdom", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[19]/div/div/div[3]/div[1]/div[2]'),
        ("1 Dia - Disney Basico Epcot", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[27]/div/div/div[3]/div[1]/div[2]'),
        ("2 Dias - Disney World Bsico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[34]/div/div/div[3]/div[1]/div[2]'),
        ("3 Dias - Disney World Basico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[42]/div/div/div[3]/div[1]/div[2]'),
        ("4 Dias - Disney World Basico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[56]/div/div/div[3]/div[1]/div[2]'),
        ("4 Dias - Disney Promocional",'/html/body/div[4]/div/div[1]/div[2]/div[1]/div[49]/div/div/div[3]/div[1]/div[2]'),
        ("5 Dias - Disney World Basico",'/html/body/div[4]/div/div[1]/div[2]/div[1]/div[63]/div/div/div[3]/div[1]/div[2]'),
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
                # Tente localizar o elemento com o preço
                wait = WebDriverWait(driver, 5)
                elemento_preco = driver.find_element(By.XPATH, xpath)
                preco_texto = elemento_preco.text
            except NoSuchElementException:
                # Se o elemento não for encontrado, atribua um traço "-" ao valor
                preco_texto = "-"

            # Adicione os dados a lista de dicionários
            dados.append({
                'Data_Hora_Coleta': datetime.now().strftime('%Y%m%d_%H%M%S.%f'),
                'Data_viagem': data_viagem.strftime('%Y-%m-%d'),
                'Parque': parque,
                'Preco': preco_texto
            })

    # Fechando o driver
    driver.quit()

    # Criando um DataFrame
    df = pd.DataFrame(dados)

    # Ordenando por data de viagem
    df = df.sort_values(by=['Data_viagem','Parque'])

    # Salvar em um arquivo TXT no mesmo diretório do script
    nome_arquivo_saida_txt = f'coleta_voupra_disney_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'


    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Define o caminho completo para o arquivo de saída TXT na mesma pasta que o script
    caminho_arquivo_saida_txt = os.path.join(diretorio_atual, nome_arquivo_saida_txt)

    # Salvando em um arquivo TXT no mesmo diretório que o script
    df.to_csv(caminho_arquivo_saida_txt, sep='\t', index=False)

    # Define o nome do arquivo de saída em formato JSON
    formato_data_hora = "%d%m%Y_%H%M"
    data_hora_atual = datetime.now().strftime(formato_data_hora)
    nome_arquivo_saida_json = f"coleta_voupra_disney_{data_hora_atual}.json"
    nome_arquivo_json = nome_arquivo_saida_json.replace("/", "_").replace(":", "_").replace(" ", "_")

        # Define o caminho completo para o arquivo de saída JSON na mesma pasta que o script
    caminho_arquivo_saida_json = os.path.join(nome_arquivo_json)

        # Salvando em um arquivo JSON no mesmo diretório que o script
    df.to_json(caminho_arquivo_saida_json, orient='records', date_format='iso')
    logging.info(f"Resultados salvos em {caminho_arquivo_saida_txt} e {caminho_arquivo_saida_json}")
    logging.info("Coleta finalizada.")
    # Encerrar o log
    logging.info("Coleta de preços finalizada.")


if __name__ == '__main__':
    asyncio.run(coletar_precos_voupra_disney())