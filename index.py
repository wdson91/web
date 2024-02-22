from imports import *
import asyncio
import schedule
from datetime import datetime
import pytz

async def executar_ambos(hour):
    await asyncio.gather(
        main_voupra(hour, run_once=True),
        main_vmz(hour, run_once=True),
        main_ml(hour, run_once=True)
    )
    logging.info("Aguardando a próxima execução...")

async def agendar_execucao():
    current_time = datetime.now(pytz.timezone('America/Sao_Paulo'))
    target_hours = ["7:00","11:00", "16:28", "17:00"]

    for hour in target_hours:
        if current_time.strftime("%H:%M") == hour:
            await executar_ambos(hour)
            break  # Uma vez que a tarefa é executada, não precisamos continuar verificando os outros horários

async def main():
    while True:
        await agendar_execucao()
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
