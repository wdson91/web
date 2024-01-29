import pandas as pd
import asyncio
import os
from datetime import datetime
import logging
from .vmz_disney_dias import coletar_precos_vmz_disneydias
from .vmz_disney_basicos import coletar_precos_vmz_disneybasicos


async def coletar_precos_vmz_disney():
    # Primeira parte do código - Função join_vmz
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    async def join_vmz():
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))

        formato_data_hora = "%d%m%Y_%H%M"
        data_hora_atual = datetime.now().strftime(formato_data_hora)
        # Nomes dos arquivos
        arquivo1 = os.path.join(diretorio_atual, 'precos_vmz_disney_basicos.txt')
        arquivo2 = os.path.join(diretorio_atual, 'precos_vmz_disney_dias.txt')
        nome_arquivo_json = f"coleta_vmz_disney_{data_hora_atual}.json"
        nome_arquivo_json = nome_arquivo_json.replace("/", "_").replace(":", "_").replace(" ", "_")

        # Lendo os dados dos arquivos em DataFrames
        df1 = pd.read_csv(arquivo1, sep='\t')
        df2 = pd.read_csv(arquivo2, sep='\t')

        # Concatenando os DataFrames
        df_combinado = pd.concat([df1, df2], ignore_index=True)

        # Convertendo 'Data_viagem' para datetime
        df_combinado['Data_viagem'] = pd.to_datetime(df_combinado['Data_viagem'])

        # Definindo a ordem personalizada para a coluna 'Parque'
        ordem_personalizada = [
            "1 Dia - Disney Basico Magic Kingdom",
            "1 Dia - Disney Basico Hollywood Studios",
            "1 Dia - Disney Basico Animal Kingdom",
            "1 Dia - Disney Basico Epcot",
            "2 Dias - Disney World Basico",
            "3 Dias - Disney World Basico",
            "4 Dias - Disney Promocional",
            "4 Dias - Disney World Basico",
            "5 Dias - Disney World Basico"
        ]

        # Aplicando a ordenação personalizada
        df_combinado['Parque'] = pd.Categorical(df_combinado['Parque'], categories=ordem_personalizada, ordered=True)

        # Ordenando o DataFrame primeiro por 'Data_viagem', depois por 'Parque'
        df_combinado.sort_values(by=['Data_viagem', 'Parque'], inplace=True)

        # Salvando o DataFrame combinado e ordenado em um arquivo JSON no formato desejado
        with open(nome_arquivo_json, 'w', encoding='utf-8') as json_file:
            json_file.write('[')
            for _, row in df_combinado.iterrows():
                json_file.write(f'{{"Data_Hora_Coleta":"{row["Data_Hora_Coleta"]}",'
                                f'"Data_viagem":"{row["Data_viagem"]}",'
                                f'"Parque":"{row["Parque"]}",'
                                f'"Preco":"{row["Preco"]}"}}')
                if _ != len(df_combinado) - 1:
                    json_file.write(',')
            json_file.write(']')

        logging.info(f"Os arquivos {arquivo1} e {arquivo2} foram combinados e ordenados em {nome_arquivo_json}.")

    # Segunda parte do código - Função main com chamadas assíncronas
    async def main_async():
        max_attempts = 3  # Define o número máximo de tentativas

        # Função para tentar executar uma função assíncrona com tentativas múltiplas
        async def try_execute(func):
            attempts = 0
            while attempts < max_attempts:
                try:
                    await func()
                    logging.info(f"{func.__name__} executado com sucesso.")

                    break  # Sai do loop se a função for bem-sucedida
                except Exception as e:
                    logging.error(f"Erro ao executar {func.__name__}: {e}")

                    attempts += 1
                    if attempts == max_attempts:
                        logging.error(f"Falha apos {max_attempts} tentativas para {func.__name__}")

        # Chamadas das funções com tentativas de recuperação de erro
        await try_execute(coletar_precos_vmz_disneybasicos)
        await try_execute(coletar_precos_vmz_disneydias)
        await try_execute(join_vmz)  

    # Executar a função main assíncrona
    await main_async()

if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_disney())
