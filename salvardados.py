import pandas as pd
import os
from datetime import datetime

def converter_data_hora(data_hora_str):
    formatos = ['%Y%m%d_%H%M%S.%f', '%Y-%m-%d %H:%M.%f','%Y-%m-%d %H:%M:%S.%f']  # Adicione mais formatos conforme necessário
    for formato in formatos:
        try:
            return pd.to_datetime(data_hora_str, format=formato)
        except (ValueError, TypeError):
            continue
    raise ValueError(f"Data e hora não reconhecidas: {data_hora_str}")


def salvar_dados(df, diretorio, identificador):
    """
    Salva um DataFrame em arquivos TXT e JSON.

    Parâmetros:
    df (pandas.DataFrame): O DataFrame a ser salvo.
    diretorio (str): Caminho do diretório onde os arquivos serão salvos.
    identificador (str): Um identificador para o nome do arquivo.
    """
    df['Data_Hora_Coleta'] = df['Data_Hora_Coleta'].apply(converter_data_hora)
    df['Data_Hora_Coleta'] = df['Data_Hora_Coleta'].dt.strftime('%Y-%m-%d %H:%M')
    # Ordenando por data de viagem
    df = df.sort_values(by=['Data_viagem', 'Parque'])
    

    # Salvar em TXT
    nome_arquivo_txt = f'coleta_{identificador}_{datetime.now().strftime('%d%m%Y')}.txt'
    caminho_arquivo_txt = os.path.join(diretorio, nome_arquivo_txt)
    df.to_csv(caminho_arquivo_txt, sep='\t', index=False)

    # Salvar em JSON
    nome_arquivo_json = f'coleta_{identificador}_{datetime.now().strftime('%d%m%Y')}.json'
    caminho_arquivo_json = os.path.join( nome_arquivo_json)
    df.to_json(caminho_arquivo_json, orient='records', date_format='iso')

    print(f'Arquivos salvos: {nome_arquivo_txt} e {nome_arquivo_json}')
