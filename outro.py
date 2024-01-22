import requests
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def extract_price(driver, xpath_selector):
    elemento = driver.find_element(By.XPATH, xpath_selector)
    return elemento.text if elemento else None

def save_prices(data, file_name):
    df = pd.DataFrame(data)

    if 'data' not in df.columns:
        df['data'] = df['data_hora_coleta'].dt.strftime('%d/%m/%Y')

    df['data_base'] = pd.to_datetime(df['data'], format='%d/%m/%Y') + timedelta(days=5)
    df = df[['data_hora_coleta', 'data', 'data_base', 'parque', 'preco']]

    df.to_excel(file_name, index=False)

def is_good_day(price, interval):
    limites = {
        'D0_D5': 100,
        'D6_D15': 90,
        'D16_D30': 80,
        'D31_D60': 70,
        'D61_D120': 60,
        'D120_PLUS': 50
    }
    return price <= limites[interval]

def main():
    sites = [
        ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-magic-kingdom-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Magic Kingdom'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/epcot?",  '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Epcot'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-hollywood-studios-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Hollywood Studios'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-animal-kingdom-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b', '1 Dia - Disney Básico Animal Kingdom'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/promocao-disney-world-4-park-magic/promocao-disney-world-4-park-magic?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[3]/div[1]/b', '4 Dias - Disney Promocional')
    ]

    data_atual = datetime.now().date()
    dias_para_pesquisar = 10
    precos = []

    for site_url, xpath_selector, nome_parque in sites:
        try:
            driver = webdriver.Chrome()
            for dias in range(dias_para_pesquisar):
                data_futura = data_atual + timedelta(days=dias)
                data_formatada = data_futura.strftime("%Y-%m-%d")
                url = f'{site_url}?data={data_formatada}'

                driver.get(url)

                # Extraia o preço da página usando XPath
                price_text = extract_price(driver, xpath_selector)

                if price_text is not None:
                    price = float(price_text.replace('R$', '').replace(',', '.'))
                    price_multiplicado = price * 10

                    if dias <= 5:
                        intervalo = 'D0_D5'
                    elif dias <= 15:
                        intervalo = 'D6_D15'
                    elif dias <= 30:
                        intervalo = 'D16_D30'
                    elif dias <= 60:
                        intervalo = 'D31_D60'
                    elif dias <= 120:
                        intervalo = 'D61_D120'
                    else:
                        intervalo = 'D120_PLUS'

                    bom_dia = is_good_day(price, intervalo)
                    precos.append({'data_hora_coleta': datetime.now(), 'parque': nome_parque, 'preco': price, 'bom_dia': bom_dia})

        except Exception as e:
            print(f"Erro durante a execução: {str(e)}")

        finally:
            driver.quit()

    try:
        # Encontre o melhor dia dentro de cada grupo
        df = pd.DataFrame(precos)
        grupos = df.groupby('parque')
        for nome_parque, grupo in grupos:
            melhores_dias_grupo = grupo.loc[grupo['preco'].idxmin(), 'data_hora_coleta']
            df.loc[df['parque'] == nome_parque, 'melhor_dia_grupo'] = melhores_dias_grupo
    except Exception as e:
        print(f"Erro ao analisar os dados: {str(e)}")

    finally:
        # Salve os preços em um arquivo Excel
        save_prices(precos, 'precos_ingressos.xlsx')

if __name__ == "__main__":
    main()
