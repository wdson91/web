from imports import *
from voupra.index_voupra import main_voupra
import pytz  # Importe pytz para lidar com fusos horários

# Define a lista de datas
array_datas = [5, 10, 20, 47, 65, 126]

async def agendar_execucao(target_hours):
    # Defina o fuso horário de São Paulo
    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')

    while True:
        # Obtenha a hora atual no fuso horário de São Paulo
        current_time = datetime.now(sao_paulo_tz).strftime("%H:%M")

        # Verifica se o horário atual coincide com algum dos horários alvo
        if current_time in target_hours:
            await main_voupra(current_time, array_datas, run_once=True)
            logging.info(f"A execução da main_voupra foi agendada para as {current_time}")

        # Aguarde 60 segundos antes de verificar novamente
        await asyncio.sleep(60)

async def main():
    # Defina os horários-alvo ajustados para o fuso horário de São Paulo
    target_hours = ["07:00", "11:00", "16:48", "17:00"]

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    await agendar_execucao(target_hours)

if __name__ == "__main__":
    asyncio.run(main())
