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
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',options=options)

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
                    preco_texto = elemento_preco

                    # Multiplicar o preço por 10
                    price_text = preco_texto.text
                    price_decimal = float(price_text.replace('R$', '').replace('.', '').replace(',', '.').strip())
                    new_price = round(price_decimal , 2)
                    new_price *= 10
                except NoSuchElementException:
                    

                    # Se o elemento não for encontrado, atribua um traço "-" ao valor
                    new_price = "-"

                data_hora_atual = datetime.now()
                dados.append({
                        'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"),
                        'Parque': parque,
                        'Preco': new_price
                    })
    logging.info("Coleta finalizada.")
    # Fechando o driver
    driver.quit()

    # Criando um DataFrame
    df_disneybasicos = pd.DataFrame(dados)
    print(df_disneybasicos)
    
    #inserir_dados_no_banco(df_disneybasicos, 'vmz_disney_basicos')

    logging.info("Coleta finalizada Site Vmz- Disney.")
    
    return df_disneybasicos

async def coletar_precos_vmz_disneydias():
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',options=options)
    

    waiter = 1

    def fechar_popups(driver):
        try:
            botao_fechar_selector = '.dinTargetFormCloseButtom'
            botao_fechar = WebDriverWait(driver, waiter + 4).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, botao_fechar_selector))
            )
            botao_fechar.click()
            logging.info("Pop-up fechado.")
        except Exception as e:
            logging.warning(f"Popup não encontrada")

    def scroll_to_element(driver, element):
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(waiter + 3)  # Espera para a rolagem acontecer

    def mudar_mes_ano(driver, mes, ano):
        try:
            year_select = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "year-control")))
            scroll_to_element(driver, year_select)
            year_select.click()
            driver.find_element(By.CSS_SELECTOR, f'option[value="{ano}"]').click()

            month_select = WebDriverWait(driver, waiter + 2).until(EC.element_to_be_clickable((By.ID, "month-control")))
            scroll_to_element(driver, month_select)
            month_select.click()
            driver.find_element(By.CSS_SELECTOR, f'option[value="{mes}"]').click()

            logging.info(f"Mudança para mês {mes} e ano {ano} realizada com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao mudar mês e ano: {e}")

    def encontrar_preco_data(driver, data):
        try:
            time.sleep(waiter + 9)  # Aguardar o calendário carregar
            elementos_fc_content = driver.find_elements(By.CLASS_NAME, 'fc-content')
            for elemento in elementos_fc_content:
                fc_date = elemento.find_element(By.CLASS_NAME, 'fc-date').text
                if fc_date == str(data.day):
                    calendar_event_price = elemento.find_element(By.CLASS_NAME, 'calendar-event-price')
                    price_text = calendar_event_price.text.strip()
                    price_decimal = float(price_text.replace('R$', '').replace('.', '').replace(',', '.').strip())
                    new_price = round(price_decimal * 1.10, 2)
                    return new_price
        except Exception as e:
            logging.error(f"Erro ao encontrar preço para data {data}: {e}")
            return None

    nome_pacotes = {
        2: "2 Dias - Disney World Basico",
        3: "3 Dias - Disney World Basico",
        4: "4 Dias - Disney World Basico",
        5: "5 Dias - Disney World Basico"
    }

    def processar_dias(driver, dias):
        base_url = "https://www.vmzviagens.com.br/ingressos/orlando/walt-disney-orlando/ticket-disney-basico"
        datas = [datetime.now() + timedelta(days=d) for d in [5, 10, 20, 47, 64, 126]]
        dados = []

        for dia in dias:
            logging.info(f"Coletando preços para {dia} dias.")
            nome_pacote = nome_pacotes.get(dia, f"{dia} Dias - Desconhecido")
            url_com_dias = f"{base_url}?mes=2024-01&dias={dia}"
            driver.get(url_com_dias)
            fechar_popups(driver)

            for data in datas:
                mes = data.month - 1
                ano = data.year
                mudar_mes_ano(driver, mes, ano)
                preco = encontrar_preco_data(driver, data)
                if preco:
                    data_hora_atual = datetime.now()
                    dados.append({
                        'Data_Coleta': data_hora_atual.strftime("%Y-%m-%d"),
                        'Hora_Coleta': data_hora_atual.strftime("%H:%M:%S"),
                        'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"),
                        'Parque': nome_pacote,
                        'Preco': preco
                    })
                else:
                    logging.warning(f"Preço não encontrado para {nome_pacote} em {data}")

        return dados  # Return the 'dados' list

    dias_para_processar = [2,3,4,5]
    resultados = processar_dias(driver, dias_para_processar)

    
    driver.quit()
    df_disneydias = pd.DataFrame(resultados)

    # inserir_dados_no_banco(df_disneydias, 'vmz_disney')

    logging.info("Coleta finalizada Site Vmz- Disney.")
    
    return df_disneydias

if __name__ == "__main__":
    df_disneybasicos = asyncio.run(coletar_precos_vmz_disneybasicos())
    df_disneydias = asyncio.run(coletar_precos_vmz_disneydias())
    
    df_final = pd.concat([df_disneybasicos, df_disneydias], ignore_index=True)
    print(df_final)
