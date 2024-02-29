from imports import *

async def coletar_precos_vmz_universal(hour, array_datas):
    logging.info("Iniciando coleta de preços da Universal Orlando.")
    
    sites = [
        ("https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/1-parque-1-dia-data-fixa?", '1 Dia 1 Parque - Universal Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/2-parques-1-dia-park-to-park-data-fixa?", '1 Dia 2 Parques - Universal Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/2-parques-2-dias-park-to-park-data-fixa?", '2 Dias 2 Parques - Universal Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/2-parques-compre-2-dias-e-ganhe-2-dias-gratis-park-to-park?", '4 Dias 2 Parques - Universal Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/3-parques-compre-2-dias-e-ganhe-2-dias-gratis-park-to-park?", '4 Dias 3 Parques - Universal Orlando')
    ]

    url_14_dias = "https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/14-dias-flexiveis-uso-em-2024?"
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
    
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]
    dados = []

    for data in datas:
        for url_template, parque in sites:
            logging.info(f"Coletando preços do parque {parque}.")
            site_url = f"{url_template}data={data.strftime('%Y-%m-%d')}"
            driver.get(site_url)

            try:
                preco_parcelado_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b')
                preco_avista_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]')
            except NoSuchElementException:
                try:
                    preco_parcelado_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[3]/div[2]/b')
                    preco_avista_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[3]/div[2]/span[1]')
                except NoSuchElementException:
                
                    preco_final_avista = preco_float = "-"
                else:
                    # Multiplicar o preço parcelado por 10
                    preco_parcelado = preco_parcelado_element.text.replace('R$ ', '').replace(',', '.')
                    preco_float = float(preco_parcelado) * 10
                    preco_final_avista = float(preco_avista_element.text.replace('R$ ', '').replace('.','').replace(',', '.'))
            else:    
                preco_final_avista = float(preco_avista_element.text.replace('R$ ', '').replace('.','').replace(',', '.'))
                preco_parcelado = preco_parcelado_element.text.replace('R$ ', '').replace(',', '.')
                preco_float = float(preco_parcelado) * 10
                
            dados.append({
                'Data_viagem': data.strftime("%Y-%m-%d"),
                'Parque': parque,
                'Preco_Parcelado': preco_float,
                'Preco_Avista': preco_final_avista
            })

        driver.get(url_14_dias)
        try:
            preco_parcelado_14_dias_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[1]/div[2]/b')
            preco_avista_14_dias_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[1]/div[2]/span[1]')
                
            # Convertendo o preço parcelado para float e multiplicando por 10
            preco_parcelado_14_dias = preco_parcelado_14_dias_element.text.replace('R$ ', '').replace(',', '.')
            preco_final_14_dias_parcelado = float(preco_parcelado_14_dias) * 10

            
            preco_avista_14_dias = float(preco_avista_14_dias_element.text.replace('R$ ', '').replace('.','').replace(',', '.'))
            
        except NoSuchElementException:
            preco_parcelado_14_dias = preco_final_14_dias_parcelado = "-"

        
        dados.append({
            'Data_viagem': data.strftime("%Y-%m-%d"),
            'Parque': '14 Dias 3 Parques - Universal Orlando',
            'Preco_Parcelado': preco_final_14_dias_parcelado,
            'Preco_Avista': preco_avista_14_dias
        })

    driver.quit()

    df = pd.DataFrame(dados)
    

    nome_arquivo = f'universal_vmz_{datetime.now().strftime("%Y-%m-%d")}.json'
    salvar_dados(df, nome_arquivo, 'vmz', hour)
    logging.info("Coleta finalizada Site Vmz- Universal Orlando.")


if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_universal())
