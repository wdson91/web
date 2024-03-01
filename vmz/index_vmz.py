from imports import *

from .vmzdisney.vmz_disney import coletar_precos_vmz, coletar_precos_vmz_disneybasicos, coletar_precos_vmz_disneydias
from .vmzsea.vmzsea import coletar_precos_vmz_seaworld
from .vmzuniversal.vmzuniversal import coletar_precos_vmz_universal


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
async def main_vmz(hour, array_datas, run_once=False):
    if run_once:
        logging.info("Iniciando coleta de preços.")
        try:
            await asyncio.gather(
                tentar_executar(coletar_precos_vmz_disneydias,nome_pacotes,array_datas, hour),
                tentar_executar(coletar_precos_vmz_disneybasicos, array_datas, hour),
                tentar_executar(coletar_precos_vmz_seaworld, hour, array_datas),
                tentar_executar(coletar_precos_vmz, hour, array_datas),
                tentar_executar(coletar_precos_vmz_seaworld, hour, array_datas),
                tentar_executar(coletar_precos_vmz_universal, hour, array_datas)
            )
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")

if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_vmz())