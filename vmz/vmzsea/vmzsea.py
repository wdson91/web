from imports import *

diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível

# Adicionando o diretório 'docs' ao sys.path
sys.path.insert(0, diretorio_avo)

async def coletar_precos_vmz_seaworld(hour,array_datas):
    logging.info("Iniciando coleta de preços do SeaWorld.")
    # Lista de sites e nomes de parques
    sites = [
        ("https://www.vmzviagens.com.br/ingressos/orlando/seaworld-orlando/seaworld-1-dia", '1 Dia 1 Parque - SeaWorld Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/seaworld-orlando/promocao-seaworld-busch-gardens-aquatica", '3 Dias 3 Parques - SeaWorld Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/seaworld-orlando/seaworld-14-dias-estacionamento", '14 Dias 3 Parques - SeaWorld Orlando')
    ]

    # Configuração inicial do Selenium
    options = webdriver.ChromeOptions()
    #driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)

    # Definindo as datas
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    # Lista para armazenar os dados
    dados = []

    for data in datas:
        for url, parque in sites:
            logging.info(f"Coletando precos do parque {parque}.")

            driver.get(url)

            
            try:
                preco_parcelado_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div/div[1]/b')
                preco_avista_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div/div[1]/span[1]')

                # Multiplicar o preço parcelado por 10
                preco_parcelado = preco_parcelado_element.text.replace('R$ ', '').replace(',', '.')
                preco_float = float(preco_parcelado) * 10
                #preco_final_parcelado = f"R$ {preco_float:    
                
                preco_final_avista = float(preco_avista_element.text.replace('R$ ', '').replace('.','').replace(',', '.'))
                
            except NoSuchElementException:
                
                preco_final_avista = preco_float = "-"
            dados.append({
                'Data_viagem': data.strftime("%Y-%m-%d"),
                'Parque': parque,
                'Preco_Parcelado': preco_float,
                'Preco_Avista': preco_final_avista
            })


    driver.quit()

    # Criando um DataFrame
    df = pd.DataFrame(dados)
    
    nome_arquivo = f'seaworld_vmz_{datetime.now().strftime("%Y-%m-%d")}.json'
    salvar_dados(df, nome_arquivo,'vmz',hour)
    
    logging.info("Coleta finalizada Site Vmz- SeaWorld")
if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_seaworld())
