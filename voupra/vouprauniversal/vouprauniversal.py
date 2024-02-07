
from imports import *

diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível

# Adicionando o diretório 'docs' ao sys.path
sys.path.insert(0, diretorio_avo)
from insert_database import inserir_dados_no_banco

async def coletar_precos_voupra_universal():
    # Configuração inicial do Selenium
    try:
        options = webdriver.ChromeOptions()
        driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
        # Definindo as datas de viagem
        datas = [datetime.now().date() + timedelta(days=d) for d in [5, 10, 20, 47, 64, 126]]

        # Definindo os nomes dos parques e os XPaths correspondentes
        parques_xpaths = [
            ("1 Dia 1 Parque - Universal Orlando", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[34]/div/div/div[3]/div[1]/div[5]'),
            ("1 Dia 2 Parques - Universal Orlando", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[27]/div/div/div[3]/div[1]/div[5]'),
            ("2 Dias 2 Parques - Universal Orlando", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[19]/div/div/div[3]/div[1]/div[5]'),
            ("4 Dias 2 Parques - Universal Orlando", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[12]/div/div/div[3]/div[1]/div[5]'),
            ("14 Dias 3 Parques - Universal Orlando", '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[4]/div/div/div[3]/div[1]/div[5]')
        ]


        # Lista para armazenar os dados
        dados = []
        logging.info("Iniciando a coleta de precos de ingressos Universal no site Voupra.")
        for data in datas:
            for parque, xpath in parques_xpaths:
                url = f"https://www.voupra.com/estados-unidos/orlando/universal-orlando?Id=53458&DataIngresso={data.strftime('%d%%2F%m%%2F%Y')}"
                
                try:
                    driver.get(url)

                    # Tente localizar o elemento com o preço
                    wait = WebDriverWait(driver, 20)
                    elemento_preco = driver.find_element(By.XPATH, xpath)
                    preco_texto = elemento_preco.text
                    preco_final = preco_texto.replace('R$', '').replace('.', '').replace(',', '.').strip()
                    
                    preco_final = float(preco_final) * 12
                    

                except NoSuchElementException:
                    # Se o elemento não for encontrado, atribua um traço "-" ao valor
                    preco_final = "-"
                
                # Adicione os dados a lista de dicionários
                data_hora_atual = datetime.now()
                dados.append({
                        'Data_Coleta': data_hora_atual.strftime("%Y-%m-%d"),
                        'Hora_Coleta': data_hora_atual.strftime("%H:%M:%S"),
                        'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"),
                        'Parque': parque,
                        'Preco': preco_final
                    })    
         # Criando um DataFrame
        df = pd.DataFrame(dados)
        
        # Inserindo os dados no banco de dados
        inserir_dados_no_banco(df, 'voupra_universal')
        logging.info("Coleta finalizada.")
    except Exception as e:
        logging.error(f"Erro durante a coleta de preços: {e}")
    finally:
        
        # Fechando o driver
        driver.quit()


if __name__ == '__main__':
    asyncio.run(coletar_precos_voupra_universal())