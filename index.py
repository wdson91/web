import asyncio
from datetime import datetime, timedelta
import pytz
import logging

# Importe os módulos necessários para as funções main_voupra, main_vmz e main_ml
from imports import *

# Define a lista de datas
array_datas =  [5, 10, 20, 47, 65, 126]

# Define uma função assíncrona para executar as tarefas 'main_voupra', 'main_vmz' e 'main_ml' ao mesmo tempo
async def executar_ambos(hour, array_datas):
    await asyncio.gather(
        main_voupra(hour, array_datas, run_once=True),  # Executa a função main_voupra com o argumento hour
        main_vmz(hour, array_datas, run_once=True),     # Executa a função main_vmz com o argumento hour
        main_ml(hour, array_datas, run_once=True)        # Executa a função main_ml com o argumento hour
    )
    logging.info("Aguardando a próxima execução...")  # Registra uma mensagem de log

# Define uma função assíncrona para agendar a execução das tarefas em horários específicos
async def agendar_execucao():
    while True:
        current_time = datetime.now(pytz.timezone('America/Sao_Paulo'))  # Obtém a hora atual com o fuso horário de São Paulo
        target_hours = ["07:00", "11:00", "14:00", "17:00"]  # Lista de horários-alvo para execução das tarefas

        # Itera sobre os horários-alvo
        for hour in target_hours:
            target_time = datetime.strptime(hour, "%H:%M")  # Converte a string de hora para um objeto datetime
            target_time -= timedelta(minutes=40)  # Subtrai 30 minutos do horário-alvo

            # Verifica se a hora atual corresponde a meia hora antes do horário-alvo
            if current_time.hour == target_time.hour and current_time.minute == target_time.minute:
                await executar_ambos(hour, array_datas)  # Executa as tarefas definidas na função 'executar_ambos'

        # Aguarda 60 segundos antes de verificar novamente os horários
        await asyncio.sleep(60)

# Define a função principal assíncrona para agendar e executar as tarefas
async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    await agendar_execucao()  # Chama a função para agendar a execução das tarefas

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(main())  # Executa a função principal 'main' usando asyncio
