from imports import *

diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível

# Adicionando o diretório 'docs' ao sys.path
sys.path.insert(0, diretorio_avo)
from insert_database import inserir_dados_no_banco

# Function to calculate future dates
def get_future_date(days):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

# List of days to add to the current date

async def coletar_precos_ml_universal():
    options = webdriver.ChromeOptions()
    #driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    #driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
    chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

    driver = webdriver.Chrome()
    dados = []
    wait = WebDriverWait(driver, 5)
    days_to_add = [5, 10, 20, 47, 64, 126]
    
    xpath_pairs = [
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[1]/button[1]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','1 Dia 1 Parque - Universal Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[1]/button[1]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','1 Dia 2 Parques - Universal Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[1]/button[2]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','2 Dias 2 Parques - Universal Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','4 Dias 2 Parques - Universal Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','4 Dias 3 Parques - Universal Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','14 Dias 3 Parques - Universal Orlando')
                
                # Add other pairs as needed
            ]
    try:
    
        for days in days_to_add:
            future_date = get_future_date(days)
            url = f"https://www.vamonessa.com.br/ingressos/Orlando/7?destination=Orlando&destinationCode=2&destinationState=&destinationStateCode=&date={future_date}"
            driver.get(url)
            time.sleep(5)
            
            for button_xpath, price_xpath, park_name in xpath_pairs:
                # Scroll to button and click
                button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(2) 

                try:
                    button.click()
                except ElementClickInterceptedException:
                    
                    driver.execute_script("arguments[0].click();", button)

                try:
                    price_element = wait.until(EC.presence_of_element_located((By.XPATH, price_xpath)))
                    driver.execute_script("arguments[0].scrollIntoView();", price_element)
                    time.sleep(4)
                    price_text = price_element.text
                except TimeoutException:
                    price_text = '-'
                if price_text != '-':
                    price_number_str = price_text.replace("R$", "").replace(",", ".").strip()
                # Additional code to process and print the price
                if "R$" in price_text:
                    price_number_str = price_text.replace("R$", "").replace(",", ".").strip()
                    try:
                        price_number = float(price_number_str)
                        multiplied_price = price_number * 10
                        formatted_price = "{:.2f}".format(multiplied_price)
                        #print(f"{park_name}: {formatted_price}")
                    except ValueError:
                        print(f"Error converting price for {park_name}: {price_text}")
                    # ...
                data_hora_atual = datetime.now()        
                dados.append({

                        'Data_viagem': (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d"),
                        'Parque': park_name,
                        'Preco': formatted_price 
                    })
                

        
                
    except TimeoutException as e:
        logging.error("Erro: Elemento não encontrado ou tempo de espera excedido", e)
    except Exception as e:
        logging.error("Erro inesperado:", e)
    finally:
                
                driver.quit()
                df = pd.DataFrame(dados)
        

                # Inserindo os dados no banco de dados
                #inserir_dados_no_banco(df, 'ml_universal')
                
                nome_arquivo = f'universal_ml_{datetime.now().strftime("%Y-%m-%d")}.json'
                salvar_dados(df, nome_arquivo,'ml')
                logging.info("Coleta de preços ML Disney finalizada")
if __name__ == '__main__':
    asyncio.run(coletar_precos_ml_universal())
