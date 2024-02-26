from imports import *

diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível

# Adicionando o diretório 'docs' ao sys.path
sys.path.insert(0, diretorio_avo)

# Function to calculate future dates
def get_future_date(days):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

async def coletar_precos_ml_disney(hour,array_datas):
    logging.info("Iniciando a coleta de preços ML Disney")
    options = webdriver.ChromeOptions()
    # driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
    
    dados = []
    wait = WebDriverWait(driver, 6)
    
    try:
    
        for days in array_datas:
            future_date = get_future_date(days)
            logging.info(f"Processando data: {future_date}")
            url = f"https://www.vamonessa.com.br/ingressos/WALT%20DISNEY%20WORLD/6?destination=Orlando&destinationCode=2&destinationState=Florida&destinationStateCode=2&date={future_date}&utm_source=Destaque-Advert&utm_medium=Ingressos+Disney+15-03-2022&utm_campaign=Ingressos+para+Disney&utm_id=Walt+Disney+World"
            driver.get(url)
            time.sleep(5)
            
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
            ]

            

            for button_xpath, price_xpath, park_name in xpath_pairs:
                try:
                        button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
                        driver.execute_script("arguments[0].scrollIntoView();", button)
                        time.sleep(2)  # Permitir tempo para quaisquer elementos carregados preguiçosamente
                        button.click()
                except TimeoutException:
                        logging.error(f"Tempo esgotado ao tentar localizar o botão para {park_name}")
                        continue  # Ir para o próximo parque se não conseguir localizar o botão
                except ElementClickInterceptedException:
                        logging.error(f"Erro ao clicar no botão para {park_name}")
                        continue  # Ir para o próximo parque se não conseguir clicar no botão

                try:
                    price_element = wait.until(EC.presence_of_element_located((By.XPATH, price_xpath)))
                    driver.execute_script("arguments[0].scrollIntoView();", price_element)
                    time.sleep(4)
                    price_text = price_element.text

                    if price_text != '-':
                        price_number_str = price_text.replace("R$", "").replace(",", ".").strip()
                        price_number = float(price_number_str)
                        multiplied_price = price_number * 10
                    else:
                        multiplied_price = '-'

                except TimeoutException:
                    logging.error(f"Tempo esgotado ao tentar obter o preço para {park_name}")
                    multiplied_price = '-'
                except ValueError:
                    logging.error(f"Erro ao converter preço para {park_name}: {price_text}")
                    print(f"Erro ao converter preço para {park_name}: {price_text}")
                    multiplied_price = '-'

                dados.append({
                    'Data_viagem': (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d"),
                    'Parque': park_name,
                    'Preco': multiplied_price
                })
        
                
    except TimeoutException as e:
                logging.error("Erro: Elemento não encontrado ou tempo de espera excedido", e)
    except Exception as e:
        logging.error("Erro inesperado:", e)
    finally:
                driver.quit()

                df = pd.DataFrame(dados)
                
                nome_arquivo = f'disney_ml_{datetime.now().strftime("%Y-%m-%d")}.json'
                salvar_dados(df, nome_arquivo,'ml',hour)
                
                logging.info("Coleta de preços ML Disney finalizada")
                
if __name__ == '__main__':
    asyncio.run(coletar_precos_ml_disney())