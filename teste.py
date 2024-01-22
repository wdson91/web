from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import pandas as pd

def extract_price(driver, xpath_selector):
    wait = WebDriverWait(driver, 20)
    elemento = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_selector)))
    return elemento.text

def save_prices(data, file_name):
    df = pd.DataFrame(data)
    df['data_hora_coleta'] = datetime.now()
    df['data_base'] = df['data'].apply(lambda x: datetime.strptime(x, "%d/%m/%Y") + timedelta(days=5))
    df = df[['data_hora_coleta', 'data', 'data_base', 'parque', 'preco']]
    df.to_excel(file_name, index=False)

def close_popup(driver):
    try:
        popup = driver.find_element(By.CSS_SELECTOR, '#dinTargetFormDialog1')
        if popup.is_displayed():
            driver.find_element(By.CSS_SELECTOR, '#dinTargetFormDialog1 > div.dinTargetFormCloseButtom').click()
    except Exception as e:
        pass

def main():
    sites = [
        ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-magic-kingdom-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Magic Kingdom')
    ]

    data_atual = datetime.now().date()

    # Número de dias que você deseja pesquisar
    dias_para_pesquisar = 120

    precos = []

    for site_url, xpath_selector, nome_parque in sites:
        driver = webdriver.Chrome()
        try:
            for dias in range(dias_para_pesquisar):
                data_futura = data_atual + timedelta(days=dias)
                data_formatada = data_futura.strftime("%Y-%m-%d")
                url = f'{site_url}?data={data_formatada}'

                driver.get(url)
                price_text = extract_price(driver, xpath_selector)
                price = float(price_text.replace('R$', '').replace(',', '.'))
                price_multiplicado = price * 10

                precos.append({'data': data_futura.strftime("%d/%m/%Y"), 'parque': nome_parque, 'preco': price_multiplicado})

                close_popup(driver)

        except Exception as e:
            pass
        finally:
            save_prices(precos, 'precos_ingressos.xlsx')
            driver.quit()

if __name__ == "__main__":
    main()
