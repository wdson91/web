import asyncio
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

async def coletar_precos_vmz_seaworld():

    # Lista de sites e nomes de parques
    sites = [
        ("https://www.vmzviagens.com.br/ingressos/orlando/seaworld-orlando/seaworld-1-dia", '1 Dia 1 Parque - SeaWorld Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/seaworld-orlando/promocao-seaworld-busch-gardens-aquatica", '3 Dias 3 Parques - SeaWorld Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/seaworld-orlando/seaworld-14-dias-estacionamento", '14 Dias 3 Parques - SeaWorld Orlando')
    ]

    # Configuração inicial do Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Definindo as datas
    datas = [datetime.now().date() + timedelta(days=d) for d in [5, 10, 20, 47, 64, 126]]

    # Lista para armazenar os dados
    dados = []

    for data in datas:
        for url, parque in sites:
            driver.get(url)

            try:
                # Tente localizar o elemento com o preço
                wait = WebDriverWait(driver, 10)
                xpath_selector = '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div/div[1]/b'
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
            dados.append({'Data_Hora_Coleta': datetime.now(), 'Data_viagem': data.strftime("%Y-%m-%d"), 'Parque': parque, 'Preço': preco_texto})

    # Fechando o driver
    driver.quit()

    # Criando um DataFrame
    df = pd.DataFrame(dados)

    # Ordenando o DataFrame pelas datas da viagem e pelo nome do parque
    df['Data_viagem'] = pd.to_datetime(df['Data_viagem'])
    df = df.sort_values(by=['Data_viagem', 'Parque'])

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Define o nome do arquivo de saída
    nome_arquivo_saida = "precos_vmz_seaworld.txt"

    # Define o caminho completo para o arquivo de saída na mesma pasta que o script
    caminho_arquivo_saida = os.path.join(nome_arquivo_saida)

    # Salvando em um arquivo TXT no mesmo diretório que o script
    df.to_csv(caminho_arquivo_saida, sep='\t', index=False)

    nome_arquivo_saida_json = "precos_vmz_seaworld.json"

    # Define o caminho completo para o arquivo de saída JSON na mesma pasta que o script
    caminho_arquivo_saida_json = os.path.join(diretorio_atual, nome_arquivo_saida_json)

    # Salvando em um arquivo JSON no mesmo diretório que o script
    df.to_json(caminho_arquivo_saida_json, orient='records', date_format='iso')

if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_seaworld())
