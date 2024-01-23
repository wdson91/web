import asyncio
from join import join_dmz
from vmz_disney_basicos import coletar_precos_vmz_dineybasicos
from vmz_disney_dias import coletar_precos_vmz_dineydias

async def main():
    max_attempts = 3  # Define o número máximo de tentativas

    # Função para tentar executar uma função assíncrona com tentativas múltiplas
    async def try_execute(func):
        attempts = 0
        while attempts < max_attempts:
            try:
                await func()
                break  # Sai do loop se a função for bem-sucedida
            except Exception as e:
                print(f"Erro ao executar {func.__name__}: {e}")
                attempts += 1
                if attempts == max_attempts:
                    print(f"Falha após {max_attempts} tentativas para {func.__name__}")

    # Chamadas das funções com tentativas de recuperação de erro
    #await try_execute(coletar_precos_vmz_dineybasicos)
    await try_execute(coletar_precos_vmz_dineydias)
    await try_execute(join_dmz)

# Executar a função main
asyncio.run(main())
