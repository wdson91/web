import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Configuração inicial do Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Definindo as datas de viagem
datas_viagem = [datetime.now().date() + timedelta(days=d) for d in [5, 10, 20, 47, 65, 126]]

# Definindo os nomes dos parques e os XPaths correspondentes
parques_xpaths = [
    ("1 Dia - Disney Básico Magic Kingdom", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[4]/div/div/div[3]/div[1]/div[2]'),
    ("1 Dia - Disney Básico Hollywood Studios", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[12]/div/div/div[3]/div[1]/div[2]'),
    ("1 Dia - Disney Básico Animal Kingdom", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[19]/div/div/div[3]/div[1]/div[2]'),
    ("1 Dia - Disney Básico Epcot", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[27]/div/div/div[3]/div[1]/div[2]'),
    ("2 Dias - Disney World Básico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[34]/div/div/div[3]/div[1]/div[2]'),
    ("3 Dias - Disney World Básico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[42]/div/div/div[3]/div[1]/div[2]'),
    ("4 Dias - Disney World Básico", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[56]/div/div/div[3]/div[1]/div[2]'),
    ("4 Dias - Disney Promocional",'/html/body/div[4]/div/div[1]/div[2]/div[1]/div[49]/div/div/div[3]/div[1]/div[2]'),
    ("5 Dias - Disney World Básico",'/html/body/div[4]/div/div[1]/div[2]/div[1]/div[63]/div/div/div[3]/div[1]/div[2]'),
]

# Cores ANSI para os grupos de datas
cores = {
    '5 Dias': '\033[91m',   # Vermelho
    '10 Dias': '\033[92m',  # Verde
    '20 Dias': '\033[93m',  # Amarelo
    '47 Dias': '\033[94m',  # Azul
    '65 Dias': '\033[95m',  # Roxo
    '126 Dias': '\033[96m'  # Ciano
}

# Lista para armazenar os dados
dados = []

for data_viagem in datas_viagem:
    for parque, xpath in parques_xpaths:
        url = f"https://www.voupra.com/estados-unidos/orlando/disney-world?Id=49824&DataIngresso={data_viagem.strftime('%d%%2F%m%%2F%Y')}"
        driver.get(url)

        try:
            # Tente localizar o elemento com o preço
            wait = WebDriverWait(driver, 10)
            elemento_preco = driver.find_element(By.XPATH, xpath)
            preco_texto = elemento_preco.text
        except NoSuchElementException:
            # Se o elemento não for encontrado, atribua um traço "-" ao valor
            preco_texto = "-"

        # Determine a cor com base na diferença de datas
        diferenca_datas = (data_viagem - datetime.now().date()).days
        cor = cores.get(f'{diferenca_datas} Dias', '')

        # Adicione os dados a lista de dicionários
        dados.append({
            'Data_Hora_Coleta': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'Data_viagem': data_viagem.strftime('%Y-%m-%d'),
            'Parque': parque,
            'Preço': cor + preco_texto + '\033[0m'  # Reset da cor
        })

# Fechando o driver
driver.quit()

# Criando um DataFrame
df = pd.DataFrame(dados)

# Ordenando por data de viagem
df = df.sort_values(by=['Data_viagem', 'Parque'])

# Salvando em um arquivo TXT
df.to_csv('precos_ingressos_voupra.txt', sep='\t', index=False)

print(df)