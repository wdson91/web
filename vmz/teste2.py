import asyncio
from datetime import datetime
import sys
import os
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(current_dir, 'vmzdisney'))
sys.path.append(os.path.join(current_dir, 'vmzuniversal'))
sys.path.append(os.path.join(current_dir, 'vmzsea'))

# Importe as funções que deseja executar
from vmz_disney_basicos import coletar_precos_vmz_dineybasicos
from vmz_disney_dias import coletar_precos_vmz_dineydias
from vmzsea import coletar_precos_vmz_seaworld
from vmzuniversal import coletar_precos_vmz_universal

async def main():
    # Execute as funções assíncronas em sequência
    #await coletar_precos_vmz_dineybasicos()
    #await coletar_precos_vmz_dineydias()
    await coletar_precos_vmz_seaworld()
    await coletar_precos_vmz_universal()

    # Diretório atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    data_hora_atual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Diretório de destino para os arquivos JSON
    destino_json_pesquisa = os.path.join(diretorio_atual, f'vmz_pesquisa_{data_hora_atual}')

    # Verifique se a pasta "json_pesquisa" existe e crie-a se não existir
    if not os.path.exists(destino_json_pesquisa):
        os.makedirs(destino_json_pesquisa)

    # Lista dos nomes dos arquivos JSON gerados
    nomes_arquivos_json = ['precos_vmz_seaworld.json', 'precos_vmz_universal.json']

    # Mova os arquivos JSON para a pasta "vmz_pesquisa"
    for nome_arquivo_json in nomes_arquivos_json:
        origem_arquivo_json = os.path.join(current_dir, nome_arquivo_json)
        destino_arquivo_json = os.path.join(destino_json_pesquisa, nome_arquivo_json)
        shutil.move(origem_arquivo_json, destino_arquivo_json)

    # Mova o arquivo 'precos_vmz_seaworld.json' para a pasta "vmz_pesquisa"
    origem_arquivo_seaworld = os.path.join(current_dir, 'vmzsea', 'precos_vmz_seaworld.json')
    destino_arquivo_seaworld = os.path.join(destino_json_pesquisa, 'precos_vmz_seaworld.json')
    shutil.move(origem_arquivo_seaworld, destino_arquivo_seaworld)

if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main())
