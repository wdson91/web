from imports import *

diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível

# Adicionando o diretório 'docs' ao sys.path
sys.path.insert(0, diretorio_avo)
from insert_database import inserir_dados_no_banco
async def coletar_precos_voupra_sea():
    
    
    # Lista de datas a serem consideradas
    datas = [datetime.now().date() + timedelta(days=d) for d in [5, 10, 20, 47, 64, 126]]

    # URL base
    base_url = "https://www.voupra.com/estados-unidos/orlando/seaworld?Id=58825&Busca=true&DataTemporada="

    # Mapeamento de nomes desejados
    mapeamento_nomes = {
        "Ingresso 1 Dia SeaWorld - Adulto ou Criança": "1 Dia 1 Parque - SeaWorld Orlando",
        "Ingresso 3 Dias SeaWorld Parks com 3 Parques - Adulto ou Criança": "3 Dias 3 Parques - SeaWorld Orlando",
        "Ingresso 14 Dias SeaWorld Parks com 3 Parques - Adulto ou Criança": "14 Dias 3 Parques - SeaWorld Orlando"
    }

    dados = []

    # Iniciar o loop pelas datas
    for data in datas:
        try:
            # Montar a URL com a data atual do loop
            url = base_url + data.strftime('%d%%2F%m%%2F%Y')
            driver.get(url)

            # Usar WebDriverWait
            wait = WebDriverWait(driver, 10)  # Esperar até 10 segundos

            # Aguardar até que os elementos estejam presentes
            produtos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "compra_expressa_item")))

            # Inicializar um dicionário para armazenar os preços
            precos = {}

            # Loop pelos produtos
            for produto in produtos:
                try:
                    # Extraindo o título do produto
                    titulo = produto.find_element(By.CLASS_NAME, "produto_titulo")
                    titulo_texto = titulo.text

                    # Extraindo o preço do produto
                    preco = produto.find_element(By.CLASS_NAME, "produto_preco_padrao")
                    driver.execute_script("arguments[0].classList.remove('d-none');", preco)
                    preco_texto = preco.text

                    # Removendo 'R$' e substituindo vírgulas por pontos
                    preco_texto = preco_texto.replace('R$', '').replace(',', '.').strip()

                    # Removendo pontos usados como separadores de milhar
                    preco_texto = preco_texto.replace('.', '', preco_texto.count('.') - 1)

                    # Convertendo para float e formatando
                    preco_float = float(preco_texto)
                    preco_formatado = round(preco_float, 2)

                    # Adicionando o preço ao dicionário
                    precos[titulo_texto] = preco_formatado

                except Exception as e:
                    logging.error("Erro ao processar produto:", e)

            # Loop pelos nomes desejados
            for nome, nome_desejado in mapeamento_nomes.items():
                if nome in precos:
                    preco = precos[nome]
                else:
                    preco = ''

                # Adicionar os dados à lista
                dados.append({
                    'Data_Coleta': datetime.now().strftime("%Y-%m-%d"),
                    'Hora_Coleta': datetime.now().strftime("%H:%M:%S"),
                    'Data_viagem': data.strftime("%Y-%m-%d"),
                    'Parque': nome_desejado,
                    'Preco': preco
                })

        except Exception as e:
            logging.error("Erro ao processar data:", e)

    # Fechar o driver
    driver.quit()
    
    # Criar um DataFrame com os dados
    df = pd.DataFrame(dados)
    
    # Inserir os dados no banco de dados
    inserir_dados_no_banco(df, 'voupra_seaworld')


if __name__ == "__main__":
    asyncio.run(coletar_precos_voupra_sea())
