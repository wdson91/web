import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Configuração do logger
logging.basicConfig(filename='pesquisa_ingressos.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_price(driver, xpath_selector):
    # Aguarde até que o elemento com o XPath especificado esteja presente e visível
    wait = WebDriverWait(driver, 20)
    elemento = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_selector)))

    # Obtenha o texto do elemento
    return elemento.text

def save_prices(data, file_name):
    with open(file_name, 'w') as file:
        for item in data:
            preco_formatado = round(item["preco"], 2)
            # Adicione o nome do parque ao arquivo
            file.write(f'Data: {item["data"]}, Parque: {item["parque"]},  Preço: R$ {preco_formatado:.2f}\n')

def main():
    driver = webdriver.Firefox()

    try:
        sites = [
            ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-magic-kingdom-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Magic Kingdom'),
            ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/epcot?",  '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Epcot'),
            ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-hollywood-studios-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Hollywood Studios'),
            ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-animal-kingdom-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Animal Kingdom'),
            ("https://www.vmzviagens.com.br/ingressos/orlando/promocao-disney-world-4-park-magic/promocao-disney-world-4-park-magic?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[3]/div[1]/b', '4 Dias - Disney Promocional')
            # Adicione outros sites, XPaths e nomes de parques conforme necessário
        ]

        # Número de dias que você deseja adicionar
        dias_para_adicionar = [5,15,30,60,120]

        # Obtenha a data atual
        data_atual = datetime.now().date()

        precos = []

        for site_url, xpath_selector, nome_parque in sites:
            for dias in dias_para_adicionar:
                # Adicione o número de dias desejado à data atual
                data_futura = data_atual + timedelta(days=dias)

                # Formate a data futura no formato desejado (yyyy-mm-dd)
                data_formatada = data_futura.strftime("%Y-%m-%d")

                # Construa a URL com a data dinâmica
                url = f'{site_url}?data={data_formatada}'

                logging.info(f'Pesquisando em {url} para {nome_parque} na data {data_futura.strftime("%d/%m/%Y")}.')

                driver.get(url)

                # Extraia o preço da página usando XPath
                price_text = extract_price(driver, xpath_selector)

                # Remova o símbolo da moeda e a vírgula, em seguida, converta para float
                price = float(price_text.replace('R$', '').replace(',', '.'))

                # Multiplique o preço por 10
                price_multiplicado = price * 10

                precos.append({'data': data_futura.strftime("%d/%m/%Y"), 'parque': nome_parque, 'preco': price_multiplicado})

                logging.info(f'Preço encontrado: R$ {price:.2f}. Preço multiplicado por 10: R$ {price_multiplicado:.2f}')

        # Salve os preços em um arquivo
        save_prices(precos, 'precos_ingressos.xlsx ')

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
