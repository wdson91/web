import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

async def coletar_precos_vmz_dineybasicos():
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
    datas = [datetime.now().date() + timedelta(days=d) for d in [5,10,20,47,64,126]]

    # Lista para armazenar os dados
    dados = []

    # Lista de parques e XPaths na sequência desejada
    parques_xpaths = [
        ("1 Dia - Disney Básico Magic Kingdom", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b'),
        ("1 Dia - Disney Básico Hollywood Studios", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b'),
        ("1 Dia - Disney Básico Animal Kingdom", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b'),
        ("1 Dia - Disney Básico Epcot", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b'),
        ("2 Dias - Disney World Básico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[34]/div/div/div[3]/div[1]/div[2]'),
        ("3 Dias - Disney World Básico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[42]/div/div/div[3]/div[1]/div[2]'),
        ("4 Dias - Disney World Básico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[56]/div/div/div[3]/div[1]/div[2]'),
        ("4 Dias - Disney Promocional",'//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[3]/div[1]/b'),
        ("5 Dias - Disney World Básico",'/html/body/div[4]/div/div[1]/div[2]/div[1]/div[63]/div/div/div[3]/div[1]/div[2]'),
    ]

    # Criar um dicionário para mapear os nomes dos parques para os URLs correspondentes
    parque_url_map = {parque: url for url, xpath, parque in sites}

    for data in datas:
        for parque, xpath_selector in parques_xpaths:
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
                dados.append({'Data_Hora_Coleta': datetime.now(), 'Data_viagem': data.strftime("%Y-%m-%d"), 'Parque': parque, 'Preço': preco_texto})

    # Fechando o driver
    driver.quit()

    # Criando um DataFrame
    df = pd.DataFrame(dados)

    # Ordenando o DataFrame pelas datas da viagem e pelo nome do parque
    df['Data_viagem'] = pd.to_datetime(df['Data_viagem'])
    df = df.sort_values(by=['Data_viagem', 'Parque'])

    # Salvando em um arquivo TXT
    df.to_csv('precos_vmz_disney.txt', sep='\t', index=False)

    print(df)


    return