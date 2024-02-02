import asyncio
import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import os
import logging

# Função para formatar o preço
def formatar_preco(preco):
    if isinstance(preco, float):
        preco_formatado = round(preco, 2)
        
        return preco_formatado
    else:
        try:
            preco_float = float(preco.replace('R$', '').replace(',', '.').strip())
            preco_formatado = round(preco_float, 2)
            
            return preco_formatado
        except ValueError:
            return preco


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível

# Adicionando o diretório 'docs' ao sys.path
sys.path.insert(0, diretorio_avo)
from salvardados import salvar_dados
from insert_database import inserir_dados_no_banco

async def coletar_precos_vmz_universal():
    logging.info("Iniciando coleta de preços da Universal Orlando.")
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
            logging.info(f"Coletando preços do parque {parque}.")
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
                preco_final = f"R$ {preco_float:.2f}"
               
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
    
    # Coleta de preços para 14 Dias 3 Parques - Universal Orlando (não dinâmico)
    driver.get(url_14_dias)
    try:
        wait = WebDriverWait(driver, 10)
        xpath_selector = '//*[@id="__layout"]/div/div/section/article[1]/div/div/div[4]/div[1]/div[1]/div[2]/b'
        elemento_preco_14_dias = driver.find_element(By.XPATH, xpath_selector)
        preco_texto_14_dias = elemento_preco_14_dias.text
        price_decimal = float(preco_texto_14_dias.replace('R$', '').replace('.', '').replace(',', '.').strip())
        preco_final = round(price_decimal * 1.10, 2)
        
        
    except NoSuchElementException:
        preco_final = "-"

    # Adicionando o preço fixo para 14 Dias 3 Parques - Universal Orlando
    for data in datas:
        data_hora_atual = datetime.now()
        
        dados.append({
            'Data_Coleta': data_hora_atual.strftime("%Y-%m-%d"),
            'Hora_Coleta': data_hora_atual.strftime("%H:%M:%S"),
            'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"),
            'Parque': '14 Dias 3 Parques - Universal Orlando',
            'Preco':  preco_final*10
        })    
    
    driver.quit()

    # Criando um DataFrame
    df = pd.DataFrame(dados)

    # Aplicando a formatação dos preços
    df['Preco'] = df['Preco'].apply(formatar_preco)

    # Inserindo os dados no banco de dados
    inserir_dados_no_banco(df, 'vmz_universal')
    
    logging.info("Coleta finalizada Site Vmz- Universal Orlando.")

if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_universal())
