from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time

def get_price(driver, target_date, target_month):
    # Acesse o site
    driver.get(f'https://www.vmzviagens.com.br/ingressos/orlando/walt-disney-orlando/ticket-disney-basico?mes={target_month}&dias=2')

    # Obtenha a data atual
    today = datetime.now()

    # Selecione a data desejada no novo mês
    select_date(target_date, today.month, target_month, driver)

    # Espere até que o preço esteja presente
    price_selector = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.ticket-price b'))
    )

    # Obtenha o preço
    price = price_selector.text
    return price

def select_date(target_date, current_month, target_month, driver):
    while current_month != target_month:
        # Aguarde até que o botão next seja visível
        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#custom-next'))
        )

        # Clique no botão next usando JavaScript
        driver.execute_script("arguments[0].click();", next_button)

        current_month = (current_month % 12) + 1

    # Construa o seletor para a data alvo
    date_selector = f'div[data-date="{target_date}"]'

    # Aguarde até que a data desejada seja visível
    date_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, date_selector))
    )

    # Clique na data desejada usando JavaScript
    driver.execute_script("arguments[0].click();", date_element)

    # Aguarde 5 segundos
    time.sleep(5)

    # Tente fechar o popup se ele existir
    try:
        popup_close_button = driver.find_element(By.CSS_SELECTOR, '#dinTargetFormDialog1 > div.dinTargetFormCloseButtom')
        popup_close_button.click()
    except:
        pass

    # Obtenha o valor da tag br
    br_value = get_additional_info(target_date, driver)
    print(f'Valor da tag br: {br_value}')

def get_additional_info(target_date, driver):
    # Construa o seletor para a data alvo
    date_selector = f'#calendar div.fc-content [data-date="{target_date}"]'

    # Aguarde até que a data desejada seja visível
    target_date_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, date_selector))
    )

    # Clique na data desejada
    target_date_element.click()

    # Aguarde até que o elemento fc-content-selected seja visível
    target_date_selected_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'{date_selector}.fc-content-selected'))
    )

    # Aguarde até que o p com o valor desejado seja visível
    p_selector = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'{date_selector} p'))
    )

    # Obtenha o valor da tag br
    br_value = p_selector.find_element(By.TAG_NAME, 'br').text

    return br_value

def main():
    driver = webdriver.Chrome()

    try:
        # Defina a data desejada (dia e mês)
        target_date = '2'
        target_month = '2024-03'  # Mude conforme necessário

        # Obtenha o preço para a data desejada
        price = get_price(driver, target_date, target_month)

        # Imprima o preço
        print(f'O preço para a data de hoje ({target_month}-{target_date}) é: {price}')

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
