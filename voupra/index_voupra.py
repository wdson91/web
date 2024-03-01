from imports import *
from voupra.voupradisney.voupradisney import coletar_precos_voupra_disney
from voupra.vouprasea.vouprasea import coletar_precos_voupra_sea
from voupra.vouprauniversal.vouprauniversal import coletar_precos_voupra_universal


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
async def main_voupra(hour, array_datas, run_once=False):
    nome_pacotes = {
        2: "2 Dias - Disney World Basico",
        3: "3 Dias - Disney World Basico",
        4: "4 Dias - Disney World Basico",
        5: "5 Dias - Disney World Basico"
    }
    
    if run_once:
        logging.info("Iniciando coleta de preços.")
        try:
            await asyncio.gather(
                tentar_executar(coletar_precos_voupra_disney, hour, array_datas),
                tentar_executar(coletar_precos_voupra_universal, hour, array_datas),
                tentar_executar(coletar_precos_voupra_sea, hour, array_datas)
            )
        except Exception as e:
            logging.error(f"Erro ao coletar preços: {e}")

if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_voupra())