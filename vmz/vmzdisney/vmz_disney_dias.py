import asyncio
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time
import os

# Configuração inicial do Selenium
async def coletar_precos_vmz_dineydias():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    waiter = 1
    def fechar_popups(driver):
        try:
            botao_fechar_selector = '.dinTargetFormCloseButtom'
            botao_fechar = WebDriverWait(driver, waiter+4).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, botao_fechar_selector))
            )
            botao_fechar.click()
            print("Pop-up fechado.")
        except Exception as e:
            print(f"Não foi encontrado pop-up: {e}")

    def scroll_to_element(driver, element):
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(waiter+3)  # Espera para a rolagem acontecer

    def mudar_mes_ano(driver, mes, ano):

        year_select = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "year-control")))
        scroll_to_element(driver, year_select)
        year_select.click()
        driver.find_element(By.CSS_SELECTOR, f'option[value="{ano}"]').click()

        month_select = WebDriverWait(driver, waiter+2).until(EC.element_to_be_clickable((By.ID, "month-control")))
        scroll_to_element(driver, month_select)
        month_select.click()
        driver.find_element(By.CSS_SELECTOR, f'option[value="{mes}"]').click()

        

    def encontrar_preco_data(driver, data):
        time.sleep(waiter+5)  # Aguardar o calendário carregar
        elementos_fc_content = driver.find_elements(By.CLASS_NAME, 'fc-content')
        for elemento in elementos_fc_content:
            fc_date = elemento.find_element(By.CLASS_NAME, 'fc-date').text
            if fc_date == str(data.day):
                calendar_event_price = elemento.find_element(By.CLASS_NAME, 'calendar-event-price')
                price_text = calendar_event_price.text.strip()
                price_decimal = float(price_text.replace('R$', '').replace('.', '').replace(',', '.').strip())
                new_price = round(price_decimal * 1.10, 2)
                return new_price

    nome_pacotes = {
        2: "2 Dias - Disney World Básico",
        3: "3 Dias - Disney World Básico",
        4: "4 Dias - Disney World Básico",
        5: "5 Dias - Disney World Básico"
    }

    def processar_dias(driver, dias):
        base_url = "https://www.vmzviagens.com.br/ingressos/orlando/walt-disney-orlando/ticket-disney-basico"
        datas = [datetime.now() + timedelta(days=d) for d in [5, 10, 20, 47, 64,126]]
        resultados = []

        for dia in dias:
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
                    resultados.append({
                        'Data_Hora_Coleta': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                        'Data_viagem': data.strftime("%Y-%m-%d"),
                        'Parque': nome_pacote,
                        'Preço': f"R$ {preco}"
                    })
        
        return resultados

    dias_para_processar = [2, 3, 4, 5]

    resultados = processar_dias(driver, dias_para_processar)

    driver.quit()

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Define o nome do arquivo de saída
    nome_arquivo_saida = "precos_vmz_disney_dias.txt"

    # Define o caminho completo para o arquivo de saída dentro da pasta "vmzdisney"
    caminho_arquivo_saida = os.path.join(diretorio_atual,nome_arquivo_saida)

    

    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(caminho_arquivo_saida, sep='\t', index=False)
    
if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_dineydias())