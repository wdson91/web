import asyncio
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import os

async def coletar_precos_vmz_universal():

    # Lista de sites e nomes de parques
    sites = [
        ("https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/1-parque-1-dia-data-fixa?", '1 Dia 1 Parque - Universal Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/2-parques-1-dia-park-to-park-data-fixa?", '1 Dia 2 Parques - Universal Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/2-parques-2-dias-park-to-park-data-fixa?", '2 Dias 2 Parques - Universal Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/2-parques-compre-2-dias-e-ganhe-2-dias-gratis-park-to-park?", '4 Dias 2 Parques - Universal Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/3-parques-compre-2-dias-e-ganhe-2-dias-gratis-park-to-park?", '4 Dias 3 Parques - Universal Orlando')
    ]

    # URL para 14 Dias 3 Parques - Universal Orlando (não dinâmico)
    url_14_dias = "https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/14-dias-flexiveis-uso-em-2024?"
    xpath_14_dias = '//*[@id="__layout"]/div/div/section/article[1]/div/div/div[4]/div[1]/div[3]/div[2]/b'

    # Configuração inicial do Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Definindo as datas
    datas = [datetime.now().date() + timedelta(days=d) for d in [5, 10, 20, 47, 64, 126]]

    # Lista para armazenar os dados
    dados = []

    for data in datas:
        for url_template, parque in sites:
            site_url = f"{url_template}data={data.strftime('%Y-%m-%d')}"
            driver.get(site_url)

            try:
                # Tente localizar o elemento com o preço
                wait = WebDriverWait(driver, 10)
                xpath_selector = '//*[@id="__layout"]/div/div/section/article[1]/div/div/div[4]/div[1]/div[3]/div[2]/b'
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
            dados.append({'Data_Hora_Coleta': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"), 'Parque': parque, 'Preço': preco_texto})

    # Coleta de preços para 14 Dias 3 Parques - Universal Orlando (não dinâmico)
    driver.get(url_14_dias)
    try:
        wait = WebDriverWait(driver, 10)
        xpath_selector = '//*[@id="__layout"]/div/div/section/article[1]/div/div/div[4]/div[1]/div[1]/div[2]/b'
        elemento_preco_14_dias = driver.find_element(By.XPATH, xpath_selector)
        preco_texto_14_dias = elemento_preco_14_dias.text
        preco_texto_14_dias = preco_texto_14_dias.replace('R$ ', '').replace(',', '.')
        preco_float_14_dias = float(preco_texto_14_dias) * 10
        preco_texto_14_dias = f"R$ {preco_float_14_dias:.2f}"
    except NoSuchElementException:
        preco_texto_14_dias = "-"

    # Adicionando o preço fixo para 14 Dias 3 Parques - Universal Orlando
    for data in datas:
        dados.append({'Data_Hora_Coleta': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"), 'Parque': '14 Dias 3 Parques - Universal Orlando', 'Preco': preco_texto_14_dias})

    # Fechando o driver
    driver.quit()

    # Criando um DataFrame
    df = pd.DataFrame(dados)

    # Ordenando o DataFrame pelas datas da viagem e pelo nome do parque
    df['Data_viagem'] = pd.to_datetime(df['Data_viagem'], format="%Y-%m-%d")
    df = df.sort_values(by=['Data_viagem', 'Parque'])

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Define o nome do arquivo de saída em formato TXT
    nome_arquivo_saida_txt = "precos_vmz_universal.txt"

    # Define o caminho completo para o arquivo de saída TXT na mesma pasta que o script
    caminho_arquivo_saida_txt = os.path.join(diretorio_atual, nome_arquivo_saida_txt)

    # Salvando em um arquivo TXT no mesmo diretório que o script
    df.to_csv(caminho_arquivo_saida_txt, sep='\t', index=False)

    # Define o nome do arquivo de saída em formato JSON
    nome_arquivo_saida_json = "precos_vmz_universal.json"

    # Define o caminho completo para o arquivo de saída JSON na mesma pasta que o script
    caminho_arquivo_saida_json = os.path.join(nome_arquivo_saida_json)

    # Salvando em um arquivo JSON no mesmo diretório que o script
    df.to_json(caminho_arquivo_saida_json, orient='records', date_format='iso')

if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_universal())
