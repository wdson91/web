# Importando os módulos necessários
from imports import *  # Importa os módulos necessários, incluindo funções definidas em 'imports'

array_datas =  [5,10,20,47,65,126]

# Define uma função assíncrona para executar as tarefas 'main_voupra', 'main_vmz' e 'main_ml' ao mesmo tempo
async def executar_ambos(hour,array_datas):
    await asyncio.gather(
        main_voupra(hour,array_datas, run_once=True),  # Executa a função main_voupra com o argumento hour
        main_vmz(hour,array_datas, run_once=True),      # Executa a função main_vmz com o argumento hour
        main_ml(hour,array_datas, run_once=True)        # Executa a função main_ml com o argumento hour
    )
    logging.info("Aguardando a próxima execução...")  # Registra uma mensagem de log


# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(executar_ambos("00:00",array_datas))  # Executa a função principal 'main' usando asyncio
