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
datas_viagem = [datetime.now().date() + timedelta(days=d) for d in [5]]

# Definindo os nomes dos parques e os XPaths correspondentes
parques_xpaths = [
    ("1 Dia 1 Parque - SeaWorld Orlando", '/html/body/div[4]/div/div[1]/div[2]/div[12]/div/div/div[3]/div[1]/div[2]'),
    ("3 Dias 3 Parques - SeaWorld Orlando", '/html/body/div[4]/div/div[1]/div[2]/div[6]/div/div/div[3]/div[1]/div[2]'),
    ("14 Dias 3 Parques - SeaWorld Orlando", '/html/body/div[4]/div/div[1]/div[2]/div[27]/div/div/div[3]/div[1]/div[2]')
]


# Lista para armazenar os dados
dados = []

for data_viagem in datas_viagem:
    for parque, xpath in parques_xpaths:
        url = f"https://www.voupra.com/estados-unidos/orlando/seaworld?Id=58825&Busca=true&DataTemporada={data_viagem.strftime('%d%%2F%m%%2F%Y')}"
        driver.get(url)

        try:
            # Tente localizar o elemento com o preço
            wait = WebDriverWait(driver, 10)
            elemento_preco = driver.find_element(By.XPATH, xpath)
            preco_texto = elemento_preco.text
        except NoSuchElementException:
            # Se o elemento não for encontrado, atribua um traço "-" ao valor
            preco_texto = "-"

        # Adicione os dados a lista de dicionários
        dados.append({
            'Data_Hora_Coleta': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'Data_viagem': data_viagem.strftime('%Y-%m-%d'),
            'Parque': parque,
            'Preço': preco_texto
        })

# Fechando o driver
driver.quit()

# Criando um DataFrame
df = pd.DataFrame(dados)

# Ordenando por data de viagem
df = df.sort_values(by='Data_viagem')

# Salvando em um arquivo TXT
df.to_csv('precos_ingressos_voupra_sea.txt', sep='\t', index=False)

df.head()  # Exibindo as primeiras linhas do DataFrame como exemplo
