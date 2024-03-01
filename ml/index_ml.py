
from ml.ml_universal.ml_universal import coletar_precos_ml_universal
from ml.mldisney.ml_disney import coletar_precos_ml_disney
from ml.mlsea.mlsea import coletar_precos_ml_seaworld
from imports import *
# Define o número máximo de tentativas
MAX_TENTATIVAS = 3

# Define a função para tentar executar uma função até três vezes em caso de erro
async def tentar_executar(funcao, *args, **kwargs):
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        try:
            await funcao(*args, **kwargs)
            break
        except Exception as e:
            logging.error(f"Erro durante a execução da função: {e}")
            tentativas += 1
            logging.info(f"Tentativa {tentativas} de {MAX_TENTATIVAS}")

# Define a função principal assíncrona para a coleta de preços
async def main_ml(hour, array_datas, run_once=False):
    if run_once:
        logging.info("Iniciando coleta de preços.")
        
        try:
            await asyncio.gather(
                tentar_executar(coletar_precos_ml_disney, hour, array_datas),
                tentar_executar(coletar_precos_ml_seaworld, hour, array_datas),
                tentar_executar(coletar_precos_ml_universal, hour, array_datas)
            )
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços: {e}")

if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_ml())
