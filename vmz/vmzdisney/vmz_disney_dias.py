
from imports import *


diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível

# Adicionando o diretório 'docs' ao sys.path
sys.path.insert(0, diretorio_avo)
from salvardados import salvar_dados
from insert_database import inserir_dados_no_banco
# Configuração inicial do Selenium


async def coletar_precos_vmz_disneydias():
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',options=options)
    

    waiter = 1

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
        time.sleep(waiter + 3)  # Espera para a rolagem acontecer

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
            time.sleep(waiter + 9)  # Aguardar o calendário carregar
            elementos_fc_content = driver.find_elements(By.CLASS_NAME, 'fc-content')
            for elemento in elementos_fc_content:
                fc_date = elemento.find_element(By.CLASS_NAME, 'fc-date').text
                if fc_date == str(data.day):
                    calendar_event_price = elemento.find_element(By.CLASS_NAME, 'calendar-event-price')
                    price_text = calendar_event_price.text.strip()
                    price_decimal = float(price_text.replace('R$', '').replace('.', '').replace(',', '.').strip())
                    new_price = round(price_decimal * 1.10, 2)
                    return new_price
        except Exception as e:
            logging.error(f"Erro ao encontrar preço para data {data}: {e}")
            return None

    nome_pacotes = {
        2: "2 Dias - Disney World Basico",
        3: "3 Dias - Disney World Basico",
        4: "4 Dias - Disney World Basico",
        5: "5 Dias - Disney World Basico"
    }

    def processar_dias(driver, dias):
        base_url = "https://www.vmzviagens.com.br/ingressos/orlando/walt-disney-orlando/ticket-disney-basico"
        datas = [datetime.now() + timedelta(days=d) for d in [5, 10, 20, 47, 64, 126]]
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
                preco = encontrar_preco_data(driver, data)
                if preco:
                    data_hora_atual = datetime.now()
                    dados.append({
                        'Data_Coleta': data_hora_atual.strftime("%Y-%m-%d"),
                        'Hora_Coleta': data_hora_atual.strftime("%H:%M:%S"),
                        'Data_viagem': (data + timedelta(days=0)).strftime("%Y-%m-%d"),
                        'Parque': nome_pacote,
                        'Preco': preco
                    })
                else:
                    logging.warning(f"Preço não encontrado para {nome_pacote} em {data}")

        return dados  # Return the 'dados' list

    dias_para_processar = [2,3,4,5]
    resultados = processar_dias(driver, dias_para_processar)

    
    driver.quit()
    df_resultados = pd.DataFrame(resultados)

    # salvar_dados(df_resultados, diretorio_atual, 'vmz_disney_dias')
    inserir_dados_no_banco(df_resultados, 'vmz_disney')

    logging.info("Coleta finalizada Site Vmz- Disney.")

if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_disneydias())
