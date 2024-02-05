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

# Configuração inicial do Selenium


# List of days to add to the current date

async def coletar_precos_ml_disney():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    dados = []
    wait = WebDriverWait(driver, 5)
    days_to_add = [5, 10, 20, 47, 64, 126]
    try:
    
        for days in days_to_add:
            future_date = get_future_date(days)
            url = f"https://www.vamonessa.com.br/ingressos/WALT%20DISNEY%20WORLD/6?destination=Orlando&destinationCode=2&destinationState=Florida&destinationStateCode=2&date={future_date}&utm_source=Destaque-Advert&utm_medium=Ingressos+Disney+15-03-2022&utm_campaign=Ingressos+para+Disney&utm_id=Walt+Disney+World"
            driver.get(url)
            time.sleep(5)
            # XPaths for buttons and corresponding price elements
            xpath_pairs = [
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','1 Dia - Disney Basico Magic Kingdom'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','1 Dia - Disney Basico Hollywood Studios'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','1 Dia - Disney Basico Animal Kingdom'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','1 Dia - Disney Basico Epcot'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[1]/button[1]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','2 Dias - Disney World Basico'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[1]/button[2]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','3 Dias - Disney World Basico'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[1]/button[3]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','4 Dias - Disney World Basico'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[9]/div[2]/div[1]/button[1]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[9]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','4 Dias - Disney Promocional'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[1]/button[4]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','5 Dias - Disney World Basico'),
                
                # Add other pairs as needed
            ]

            # ...

            for button_xpath, price_xpath, park_name in xpath_pairs:
                # Scroll to button and click
                button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(2)  # Allow time for any lazy-loaded elements

                try:
                    button.click()
                except ElementClickInterceptedException:
                    # Use JavaScript click as fallback
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
                try:
                        price_number_str = price_text.replace("R$", "").replace(",", ".").strip()
                        if price_number_str != '-':
                            price_number = float(price_number_str)
                            multiplied_price = price_number * 10
                            formatted_price = "{:.2f}".format(multiplied_price)
                            # Resto do seu código...
                        else:
                            print(f"Price text is not valid for {park_name}: {price_text}")
                except ValueError:
                        print(f"Error converting price for {park_name}: {price_text}")
                        formatted_price = None  # Ou outro valor padrão que você desejar
                        # Resto do seu código...

                    # ...
                data_hora_atual = datetime.now()        
                dados.append({
                        'Data_Coleta': data_hora_atual.strftime("%Y-%m-%d"),
                        'Hora_Coleta': data_hora_atual.strftime("%H:%M:%S"),
                        'Data_viagem': (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d"),
                        'Parque': park_name,
                        'Preco': formatted_price 
                    })
                

        
                
    except TimeoutException as e:
                print("Error: Element not found or wait time exceeded", e)
    except Exception as e:
                print("Unexpected error:", e)
    finally:
                driver.quit()

                df = pd.DataFrame(dados)
        

                # Inserindo os dados no banco de dados
                inserir_dados_no_banco(df, 'ml_disney')

if __name__ == '__main__':
    asyncio.run(coletar_precos_ml_disney())
