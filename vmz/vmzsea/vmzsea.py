from imports import *


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível
from insert_database import inserir_dados_no_banco
# Adicionando o diretório 'docs' ao sys.path
sys.path.insert(0, diretorio_avo)
#from salvardados import salvar_dados
async def coletar_precos_vmz_seaworld():
    logging.info("Iniciando coleta de preços do SeaWorld.")
    # Lista de sites e nomes de parques
    sites = [
        ("https://www.vmzviagens.com.br/ingressos/orlando/seaworld-orlando/seaworld-1-dia", '1 Dia 1 Parque - SeaWorld Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/seaworld-orlando/promocao-seaworld-busch-gardens-aquatica", '3 Dias 3 Parques - SeaWorld Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/seaworld-orlando/seaworld-14-dias-estacionamento", '14 Dias 3 Parques - SeaWorld Orlando')
    ]

    # Configuração inicial do Selenium
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',options=options)

    # Definindo as datas
    datas = [datetime.now().date() + timedelta(days=d) for d in [5, 10, 20, 47, 64, 126]]

    # Lista para armazenar os dados
    dados = []

    for data in datas:
        for url, parque in sites:
            logging.info(f"Coletando precos do parque {parque}.")

            driver.get(url)

            try:
                # Tente localizar o elemento com o preço
                wait = WebDriverWait(driver, 10)
                xpath_selector = '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div/div[1]/b'
                elemento_preco = driver.find_element(By.XPATH, xpath_selector)
                preco_texto = elemento_preco.text

                # Multiplicar o preço por 10
                
                price_decimal = float(preco_texto.replace('R$', '').replace('.', '').replace(',', '.').strip())
                new_price = round(price_decimal * 1.10, 2)
                new_price *= 10
            except NoSuchElementException:
                # Se o elemento não for encontrado, atribua um traço "-" ao valor
                preco_texto = "-"

            # Adicione os dados a lista de dicionários
            data_hora_atual = datetime.now()
            dados.append({
                    'Data_Coleta': data_hora_atual.strftime("%Y-%m-%d"),
                    'Hora_Coleta': data_hora_atual.strftime("%H:%M:%S"),
                    'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"),
                    'Parque': parque,
                    'Preco': new_price
                })    

    driver.quit()

    # Criando um DataFrame
    df = pd.DataFrame(dados)
    
    # Inserindo os dados no banco de dados
    inserir_dados_no_banco(df, 'vmz_seaworld')
    #salvar_dados(df, diretorio_atual, 'vmz_disney_seaworld')
    
    logging.info("Coleta finalizada Site Vmz- SeaWorld")
if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_seaworld())
