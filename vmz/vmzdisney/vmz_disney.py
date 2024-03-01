from imports import *


async def coletar_precos_vmz(hour,array_datas,):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    nome_pacotes = {
        2: "2 Dias - Disney World Basico",
        3: "3 Dias - Disney World Basico",
        4: "4 Dias - Disney World Basico",
        5: "5 Dias - Disney World Basico"
    }

    # Defina sua lógica para baixar os arquivos e esperar por eles
    baixar_blob_se_existir('disney_vmz_basicos_parcial.json', 'vmz')
    baixar_blob_se_existir('disney_vmz_dias_parcial.json', 'vmz')
    
    # Carregue os dados do JSON baixado
    disney_basicos = carregar_dados_json('disney_vmz_basicos_parcial.json')
    disney_dias = carregar_dados_json('disney_vmz_dias_parcial.json')


    # Combine os dados de disney_basicos e disney_dias
    dados_combinados = disney_basicos[0]["Dados"] + disney_dias[0]["Dados"]

    df = pd.DataFrame(dados_combinados)
    
    df_sorted = df.sort_values(by=['Data_viagem', 'Parque'], ignore_index=True)
    # # Crie o DataFrame a partir dos dados formatados
    # df = pd.DataFrame(dados_formatados)
    
    nome_arquivo = f'disney_vmz_{datetime.now().strftime("%Y-%m-%d")}.json'
    
    # Salvar o dataframe concatenado em um arquivo JSON
    salvar_dados(df_sorted, nome_arquivo, 'vmz', hour)
    
    logging.info("Coleta finalizada.")



async def coletar_precos_vmz_disneybasicos(array_datas,hour):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    options = webdriver.ChromeOptions()
    #driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',options=options)
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)

    sites = [
    ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-magic-kingdom-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]', '1 Dia - Disney Basico Magic Kingdom'),
    ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/epcot?",  '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]', '1 Dia - Disney Basico Epcot'),
    ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-hollywood-studios-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]', '1 Dia - Disney Basico Hollywood Studios'),
    ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-animal-kingdom-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]', '1 Dia - Disney Basico Animal Kingdom'),
    ("https://www.vmzviagens.com.br/ingressos/orlando/promocao-disney-world-4-park-magic/promocao-disney-world-4-park-magic?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[3]/div[1]/span[1]', '4 Dias - Disney Promocional')
    # Adicione outros sites, XPaths e nomes de parques conforme necessario
]

    # Definindo as datas
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    # Lista para armazenar os dados
    dados = []

    # Percorrer cada site e coletar preços
    for site_url, xpath_selector, parque_nome in sites:
        for data in datas:
            logging.info(f"Coletando preços para {parque_nome} na data: {data}")
            url_com_data = f"{site_url}&data={data.strftime('%Y-%m-%d')}"
            driver.get(url_com_data)
            try:
                # Tente localizar o elemento com o preço
                wait = WebDriverWait(driver, 2)
                elemento_preco = driver.find_element(By.XPATH, xpath_selector)
                preco_texto = elemento_preco

                # Multiplicar o preço por 10
                price_text = preco_texto.text
                price_decimal = float(price_text.replace('R$', '').replace('.', '').replace(',', '.').strip())
                new_price = round(price_decimal , 2)
                preco_parcelado = round(price_decimal * 1.10, 2)
            except NoSuchElementException:
                # Se o elemento não for encontrado, atribua um traço "-" ao valor
                new_price = "-"
                preco_parcelado = "-"
            # Adicionar os dados coletados à lista
            dados.append({
                'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"),
                'Parque': parque_nome,
                'Preco_Parcelado': preco_parcelado,
                'Preco_Avista': new_price
            })

    logging.info("Coleta de preços finalizada.")
    
    
    
    driver.quit()
    # Criando um DataFrame
    df = pd.DataFrame(dados)
    
    salvar_dados(df, 'disney_vmz_basicos_parcial.json','vmz',hour)
    return df

async def coletar_precos_vmz_disneydias( nome_pacotes,array_datas,hour):
    
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
    
    waiter = 2
    dias_para_processar = [2, 3, 4, 5]
    def fechar_popups(driver):
        try:
            botao_fechar_selector = '.dinTargetFormCloseButtom'
            botao_fechar = WebDriverWait(driver, waiter + 4).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, botao_fechar_selector))
            )
            botao_fechar.click()
            logging.info("Pop-up fechado.")
        except Exception as e:
            logging.warning(f"Popup não encontrada")

    def scroll_to_element(driver, element):
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(waiter + 2)  # Espera para a rolagem acontecer

    def mudar_mes_ano(driver, mes, ano):
        try:
            year_select = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "year-control")))
            scroll_to_element(driver, year_select)
            year_select.click()
            driver.find_element(By.CSS_SELECTOR, f'option[value="{ano}"]').click()

            month_select = WebDriverWait(driver, waiter + 2).until(EC.element_to_be_clickable((By.ID, "month-control")))
            scroll_to_element(driver, month_select)
            month_select.click()
            driver.find_element(By.CSS_SELECTOR, f'option[value="{mes}"]').click()

            logging.info(f"Mudança para mês {mes} e ano {ano} realizada com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao mudar mês e ano: {e}")

    def encontrar_preco_data(driver, data):
        try:
            time.sleep(waiter + 7)  # Aguardar o calendário carregar
            elementos_fc_content = driver.find_elements(By.CLASS_NAME, 'fc-content')
            for elemento in elementos_fc_content:
                fc_date = elemento.find_element(By.CLASS_NAME, 'fc-date').text
                if fc_date == str(data.day):
                    calendar_event_price = elemento.find_element(By.CLASS_NAME, 'calendar-event-price')
                    price_text = calendar_event_price.text.strip()
                    preco_avista = float(price_text.replace('R$', '').replace('.', '').replace(',', '.').strip())
                    preco_parcelado = round(preco_avista * 1.10, 2)
                    
                    return preco_avista,preco_parcelado
        except Exception as e:
            logging.error(f"Erro ao encontrar preço para data {data}: {e}")
            return None

    nome_pacotes = {
        2: "2 Dias - Disney World Basico",
        3: "3 Dias - Disney World Basico",
        4: "4 Dias - Disney World Basico",
        5: "5 Dias - Disney World Basico"
    }

    def processar_dias(driver, dias,array_datas):
        base_url = "https://www.vmzviagens.com.br/ingressos/orlando/walt-disney-orlando/ticket-disney-basico"
        datas = [datetime.now() + timedelta(days=d) for d in array_datas]
        dados = []

        for dia in dias:
            logging.info(f"Coletando preços para {dia} dias.")
            nome_pacote = nome_pacotes.get(dia, f"{dia} Dias - Desconhecido")
            url_com_dias = f"{base_url}?mes=2024-01&dias={dia}"
            driver.get(url_com_dias)
            fechar_popups(driver)

            for data in datas:
                mes = data.month - 1
                ano = data.year
                mudar_mes_ano(driver, mes, ano)
                preco_avista,preco_parcelado = encontrar_preco_data(driver, data)
                if preco_avista:
                    
                    dados.append({
                        'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"),
                        'Parque': nome_pacote,
                        'Preco_Parcelado': preco_parcelado,
                        'Preco_Avista': preco_avista
                    })
                else:
                    logging.warning(f"Preço não encontrado para {nome_pacote} em {data}")

        return dados  # Return the 'dados' list
    driver.quit()
    
    dias_para_processar = [2,3,4,5]
    resultados = processar_dias(driver, dias_para_processar,array_datas)

    df = pd.DataFrame(resultados)

    salvar_dados(df, 'disney_vmz_dias_parcial.json','vmz',hour)
    
    return df


if __name__ == "__main__":
    df_final = asyncio.run(coletar_precos_vmz())