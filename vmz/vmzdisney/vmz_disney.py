import pandas as pd
import asyncio
import os
from datetime import datetime
import logging



diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Diretório de teste.py
diretorio_pai = os.path.dirname(diretorio_atual)  # Subindo um nível
diretorio_avo = os.path.dirname(diretorio_pai)  # Subindo mais um nível


from .vmz_disney_dias import coletar_precos_vmz_disneydias
from .vmz_disney_basicos import coletar_precos_vmz_disneybasicos
async def coletar_precos_vmz_disney():
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        

    # Executar a função main assíncrona
    await main_async()

if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_disney())
