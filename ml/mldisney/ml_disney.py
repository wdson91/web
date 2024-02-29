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
    wait = WebDriverWait(driver, 4)
    
    try:
    
        for days in array_datas:
            future_date = get_future_date(days)
            logging.info(f"Processando data: {future_date}")
            url = f"https://www.vamonessa.com.br/ingressos/WALT%20DISNEY%20WORLD/6?destination=Orlando&destinationCode=2&destinationState=Florida&destinationStateCode=2&date={future_date}"
            driver.get(url)
            time.sleep(4)
            
            xpath_pairs = [
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/span','1 Dia - Disney Basico Magic Kingdom'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span','1 Dia - Disney Basico Hollywood Studios'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/span','1 Dia - Disney Basico Animal Kingdom'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[1]/span','1 Dia - Disney Basico Epcot'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[1]/button[1]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[1]/span','2 Dias - Disney World Basico'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[1]/button[2]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[1]/span','3 Dias - Disney World Basico'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[1]/button[3]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[1]/span','4 Dias - Disney World Basico'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[9]/div[2]/div[1]/button[1]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[9]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[9]/div[2]/div[2]/div[2]/div[1]/div[1]/span','4 Dias - Disney Promocional'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[1]/button[4]', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[1]/span','5 Dias - Disney World Basico'),
            ]

            

            for button_xpath,  price_xpath_parcelado,price_xpath_vista, park_name in xpath_pairs:
                try:
                    button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                    time.sleep(2)
                    button.click()
                except TimeoutException:
                    logging.error(f"Tempo esgotado ao tentar localizar o botão para {park_name}")
                    dados.append({
                        'Data_viagem': (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d"),
                        'Parque': park_name,
                        'Preco_Avista': '-',
                        'Preco_Parcelado':  '-'
                    })
                    continue       
                try:
                    
                    price_element_parcelado = wait.until(EC.presence_of_element_located((By.XPATH, price_xpath_parcelado)))
                    price_element_vista = wait.until(EC.presence_of_element_located((By.XPATH, price_xpath_vista)))
                    driver.execute_script("arguments[0].scrollIntoView();", price_element_vista)
                    price_text_parcelado = price_element_parcelado.text
                    price_text_vista = price_element_vista.text
                        
                    if price_text_parcelado != '-':
                        price_number_str_parcelado = price_text_parcelado.replace("R$", "").replace(",", ".").strip()
                        price_number_parcelado = float(price_number_str_parcelado)
                        multiplied_price_parcelado = price_number_parcelado * 10
                    else:
                        multiplied_price_parcelado = '-'

                    if price_text_vista != '-':
                        price_number_str_vista = price_text_vista.replace("R$", "").replace(".", "").replace(",", ".").strip()
                        price_number_vista = float(price_number_str_vista)
                    else:
                        price_number_vista = '-'
                        
                except TimeoutException:
                    logging.error(f"Tempo esgotado ao tentar obter o preço à vista para {park_name}")
                    price_number_vista = '-'
                    multiplied_price_parcelado = '-'
                    
                
                # Adiciona os dados ao array, independentemente do botão estar presente ou não
                dados.append({
                    'Data_viagem': (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d"),
                    'Parque': park_name,
                    'Preco_Avista': price_number_vista if price_number_vista != '-' else '-',
                    'Preco_Parcelado': multiplied_price_parcelado if multiplied_price_parcelado != '-' else '-'
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