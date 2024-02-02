import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

# Configuração do Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Configuração de logs
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

# Lista de datas a serem consideradas
datas = [datetime.now().date() + timedelta(days=d) for d in [5, 10, 20, 47]]

# URL base
base_url = "https://www.voupra.com/estados-unidos/orlando/disney-world?Id=49824&DataIngresso="

# Lista de títulos de produtos desejados
produtos_desejados = [
    "Ingresso 1 Dia Magic Kingdom Disney - Adulto",
    "Ingresso 1 Dia Hollywood Studios Disney - Adulto",
    "Ingresso 1 Dia Animal Kingdom Disney - Adulto",
    "Ingresso 1 Dia Epcot Disney - Adulto",
    "Ingresso 2 Dias Disney - Adulto ",
    "Ingresso 3 Dias Disney - Adulto",
    "Ingresso 4 Dias Disney - Adulto",
    "Ingresso 4 Dias Disney para 4 Parques Diferentes - Adulto",
    "Ingresso 5 Dias Disney - Adulto"
]

# Iniciar o loop pelas datas
for data in datas:
    try:
        # Montar a URL com a data atual do loop
        url = base_url + data.strftime('%d%%2F%m%%2F%Y')
        driver.get(url)

        # Usar WebDriverWait
        wait = WebDriverWait(driver, 10)  # Esperar até 10 segundos

        # Aguardar até que os elementos estejam presentes
        produtos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "compra_expressa_item")))

        # Inicializar uma lista para armazenar os dados
        dados = []

        # Loop pelos produtos
        for produto in produtos:
            try:
                # Extraindo o título do produto
                titulo = produto.find_element(By.CLASS_NAME, "produto_titulo")
                titulo_texto = titulo.text

                # Verificando se o título está na lista de desejos
                if titulo_texto in produtos_desejados:
                    # Extraindo o preço do produto
                    preco = produto.find_element(By.CLASS_NAME, "produto_preco_padrao")
                    driver.execute_script("arguments[0].classList.remove('d-none');", preco)
                    preco_texto = preco.text

                    # Removendo 'R$' e substituindo vírgulas por pontos
                    preco_texto = preco_texto.replace('R$', '').replace(',', '.').strip()

                    # Removendo pontos usados como separadores de milhar
                    preco_texto = preco_texto.replace('.', '', preco_texto.count('.') - 1)

                    # Convertendo para float e formatando
                    preco_float = float(preco_texto)
                    preco_formatado = round(preco_float, 2)

                    # Adicionar os dados à lista
                    dados.append({
                        'Data_Coleta': datetime.now().strftime("%Y-%m-%d"),
                        'Hora_Coleta': datetime.now().strftime("%H:%M:%S"),
                        'Data_viagem': data.strftime("%Y-%m-%d"),
                        'Parque': titulo_texto,
                        'Preco': preco_formatado
                    })

            except Exception as e:
                logging.error("Erro ao processar produto:", e)

        # Imprimir os dados coletados para a data atual do loop
        logging.info("Dados para a data: %s", data.strftime("%Y-%m-%d"))
        for dado in dados:
            logging.info(dado)

    except Exception as e:
        logging.error("Erro ao processar data:", e)

# Fechar o driver
driver.quit()
