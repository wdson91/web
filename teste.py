from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.voupra.com/estados-unidos/orlando/disney-world?Id=49824&DataIngresso=06%2F02%2F2024")

# Usando WebDriverWait
wait = WebDriverWait(driver, 10)  # Esperar até 10 segundos


    # Aguardando até que os elementos estejam presentes
produtos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "compra_expressa_item")))

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

for produto in produtos:
    try:
        # Extraindo o título do produto
        titulo = produto.find_element(By.CLASS_NAME, "produto_titulo")
        titulo_texto = titulo.text

        # Verificando se o título está na lista de desejos
        # ...

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
            print("Título do Produto:", titulo_texto)
            print("Preço:", preco_formatado)
            print("-----------")

# ...

    except Exception as e:
        print("Erro ao processar produto:", e)


