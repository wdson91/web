# Importando os módulos necessários
from imports import *  # Importa os módulos necessários, incluindo funções definidas em 'imports'

array_datas =  [5, 10, 20, 47, 65, 126]

# Define uma função assíncrona para executar as tarefas 'main_voupra', 'main_vmz' e 'main_ml' ao mesmo tempo
async def executar_ambos(hour,array_datas):
    await asyncio.gather(
        #main_voupra(hour,array_datas, run_once=True),  # Executa a função main_voupra com o argumento hour
        main_vmz(hour,array_datas, run_once=True),      # Executa a função main_vmz com o argumento hour
        main_ml(hour,array_datas, run_once=True)        # Executa a função main_ml com o argumento hour
    )
    logging.info("Aguardando a próxima execução...")  # Registra uma mensagem de log

# Define uma função assíncrona para agendar a execução das tarefas em horários específicos
async def agendar_execucao():
    current_time = datetime.now(pytz.timezone('America/Sao_Paulo'))  # Obtém a hora atual com o fuso horário de São Paulo
    target_hours = ["07:00", "11:00", "16:48", "17:02"]  # Lista de horários-alvo para execução das tarefas

    # Itera sobre os horários-alvo
    for hour in target_hours:
        if current_time.strftime("%H:%M") == hour:  # Verifica se a hora atual corresponde a um horário-alvo
            await executar_ambos('18:00',array_datas)  # Executa as tarefas definidas na função 'executar_ambos'
            break  # Uma vez que a tarefa é executada, interrompe o loop

# Define a função principal assíncrona para agendar e executar as tarefas
async def main():
    while True:  # Loop infinito para continuar agendando e executando tarefas
        await agendar_execucao()  # Chama a função para agendar a execução das tarefas
        await asyncio.sleep(60)   # Aguarda 60 segundos antes de verificar novamente os horários

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(main())  # Executa a função principal 'main' usando asyncio
