from imports import *

diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível

# Adicionando o diretório 'docs' ao sys.path
sys.path.insert(0, diretorio_avo)


# Function to calculate future dates
def get_future_date(days):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

# List of days to add to the current date

async def coletar_precos_ml_universal(hour,array_datas):
    options = webdriver.ChromeOptions()
    # driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
    
    dados = []
    wait = WebDriverWait(driver, 5)
    
    
    xpath_pairs = [
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[1]/button[1]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/span','1 Dia 1 Parque - Universal Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[1]/button[1]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span','1 Dia 2 Parques - Universal Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[1]/button[2]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span','2 Dias 2 Parques - Universal Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[1]/span','4 Dias 2 Parques - Universal Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[1]/span','4 Dias 3 Parques - Universal Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/span','14 Dias 3 Parques - Universal Orlando')
                
                # Add other pairs as needed
            ]
    try:
    
        for days in array_datas:
            future_date = get_future_date(days)
            url = f"https://www.vamonessa.com.br/ingressos/Orlando/7?destination=Orlando&destinationCode=2&destinationState=&destinationStateCode=&date={future_date}"
            driver.get(url)
            time.sleep(5)
            
            for button_xpath, preco_parcelado, preco_avista, park_name in xpath_pairs:
                # Scroll to button and click
                button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(2) 

                try:
                    button.click()
                except ElementClickInterceptedException:
                    
                    driver.execute_script("arguments[0].click();", button)

                try:
                    price1 = wait.until(EC.presence_of_element_located((By.XPATH, preco_parcelado)))
                    price2 = wait.until(EC.presence_of_element_located((By.XPATH, preco_avista)))
                    driver.execute_script("arguments[0].scrollIntoView();",  preco_parcelado)
                    time.sleep(4)
                    price_text_1 =  preco_parcelado.text
                    price_text_2 =  preco_avista.text
                except TimeoutException:
                    price_text_1 = '-'
                    price_text_2= '-'
                if price_text_1 != '-':
                    price_number_str_1 = price_text_1.replace("R$", "").replace(",", ".").strip()
                    price_number_str_2 = price_text_2.replace("R$", "").replace(",", ".").strip()
                # Additional code to process and print the price
                if "R$" in price_text_1:
                    price_number_str_1 = price_text_1.replace("R$", "").replace(",", ".").strip()
                    price_number_str_2 = price_text_2.replace("R$", "").replace(",", ".").strip()
                    try:
                        price_number_1 = float(price_number_str_1)
                        
                        multiplied_price = price_number_1* 10
                        
                        price_number_2 = float(price_number_str_2)
                        
                    except ValueError:
                        print(f"Error converting price for {park_name}: {price_text_1}")
                    # ...
                data_hora_atual = datetime.now()        
                dados.append({

                        'Data_viagem': (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d"),
                        'Parque': park_name,
                        'Preco_Parcelado': float(multiplied_price),
                        'Preco_Avista': float(price_number_str_2),
                    })
                
    except TimeoutException as e:
        logging.error("Erro: Elemento não encontrado ou tempo de espera excedido", e)
    except Exception as e:
        logging.error("Erro inesperado:", e)
    finally:
                
                driver.quit()
                df = pd.DataFrame(dados)
                
                nome_arquivo = f'universal_ml_{datetime.now().strftime("%Y-%m-%d")}.json'
                salvar_dados(df, nome_arquivo,'ml',hour)
                logging.info("Coleta de preços ML Disney finalizada")
if __name__ == '__main__':
    asyncio.run(coletar_precos_ml_universal())
