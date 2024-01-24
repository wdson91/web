import asyncio
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(current_dir,'vmzdisney'))
sys.path.append(os.path.join(current_dir,'vmzuniversal'))
sys.path.append(os.path.join(current_dir,'vmzsea'))

# Importe as funções que deseja executar
from vmz_disney_basicos import coletar_precos_vmz_dineybasicos
from vmz_disney_dias import coletar_precos_vmz_dineydias
from vmzsea import coletar_precos_vmz_seaworld
from vmzuniversal import coletar_precos_vmz_universal

async def main():
    # Execute as funções assíncronas em sequência
    await coletar_precos_vmz_dineybasicos()
    await coletar_precos_vmz_dineydias()
    await coletar_precos_vmz_seaworld()
    await coletar_precos_vmz_universal()







if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main())
