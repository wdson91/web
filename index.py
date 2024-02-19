from imports import *



async def executar_ambos():
    
   await asyncio.sleep(30)
   
   while True:  # Adicionando um loop para continuar executando
        await asyncio.gather(
            #main_voupra(run_once=True),
            #main_vmz(run_once=True),
            main_ml(run_once=True)
        )
        logging.info("Aguardando a próxima execução...")
        await asyncio.sleep(1200)  # Aguarda por 1 hora

if __name__ == "__main__":
    asyncio.run(executar_ambos())