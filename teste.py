from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time

# Configuração inicial do Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Função para fechar pop-ups
def fechar_popups(driver):
    try:
        botao_fechar_selector = '.dinTargetFormCloseButtom'
        botao_fechar = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, botao_fechar_selector))
        )
        botao_fechar.click()
        print("Pop-up fechado.")
    except Exception as e:
        print(f"Não foi encontrado pop-up: {e}")

# Função para rolar até o elemento
def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(5)  # Espera para a rolagem acontecer

# Função para mudar o mês e o ano
def mudar_mes_ano(driver, mes, ano):
    month_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "month-control")))
    scroll_to_element(driver, month_select)
    month_select.click()
    driver.find_element(By.CSS_SELECTOR, f'option[value="{mes}"]').click()

    year_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "year-control")))
    scroll_to_element(driver, year_select)
    year_select.click()
    driver.find_element(By.CSS_SELECTOR, f'option[value="{ano}"]').click()


# Função para encontrar o preço para uma data específica
def encontrar_preco_data(driver, data):
    time.sleep(15)  # Aguardar o calendário carregar
    elementos_fc_content = driver.find_elements(By.CLASS_NAME, 'fc-content')
    for elemento in elementos_fc_content:
        fc_date = elemento.find_element(By.CLASS_NAME, 'fc-date').text
        if fc_date == str(data.day):
            calendar_event_price = elemento.find_element(By.CLASS_NAME, 'calendar-event-price')
            price_text = calendar_event_price.text.strip()
            price_decimal = float(price_text.replace('R$', '').replace('.', '').replace(',', '.').strip())
            new_price = round(price_decimal * 1.10, 2)
            return new_price

# Função para processar diferentes dias
def processar_dias(driver, dias):
    base_url = "https://www.vmzviagens.com.br/ingressos/orlando/walt-disney-orlando/ticket-disney-basico"
    datas = [datetime.now() + timedelta(days=d) for d in [5]]
    resultados = {}

    for dia in dias:
        resultados[dia] = []
        url_com_dias = f"{base_url}?mes=2024-01&dias={dia}"
        driver.get(url_com_dias)
        fechar_popups(driver)

        for data in datas:
            mes = data.month - 1  # Ajuste para o site
            ano = data.year
            mudar_mes_ano(driver, mes, ano)
            preco = encontrar_preco_data(driver, data)
            if preco:
                resultados[dia].append(f'Valor para {data.strftime("%d/%m/%Y")}: R$ {preco}')
    
    return resultados

# Dias para processar
dias_para_processar = [2, 3, 4, 5]

# Processar cada configuração de dias
resultados = processar_dias(driver, dias_para_processar)

# Fechar o navegador
driver.quit()


with open('precos_ingressos.txt', 'w') as file:
    for dia, precos in resultados.items():
        file.write(f'Resultados para {dia} dias:\n')
        for preco in precos:
            file.write(preco + '\n')
        file.write('\n')