import os
import json
from datetime import datetime
import pytz
import pandas as pd

from blob import upload_blob

# Função para carregar os dados existentes do arquivo JSON
def carregar_dados_json(nome_arquivo):
    dados = []
    if not os.path.exists(nome_arquivo) or os.stat(nome_arquivo).st_size == 0:
        with open(nome_arquivo, 'w') as file:
            json.dump([], file)
    else:
        with open(nome_arquivo, 'r') as file:
            dados = json.load(file)
    return dados

# Função para adicionar os novos dados ao arquivo JSON existente, junto com a hora da coleta
def salvar_dados( df,nome_arquivo,pasta):
    
    fuso_horario = pytz.timezone('America/Sao_Paulo')

    # Obtém a hora atual no fuso horário GMT-3
    data_hora_coleta = datetime.now(fuso_horario).strftime('%H:%M')

    
    novos_dados = df.to_dict(orient='records')
    novo_registro = {'Hora_coleta': data_hora_coleta, 'Dados': novos_dados}
    
    # Carregar os dados existentes do arquivo JSON
    dados_exist = carregar_dados_json(nome_arquivo)
    
    # Adicionar o novo registro aos dados existentes
    dados_exist.append(novo_registro)
    
    # Salvar os dados no arquivo JSON
    with open(nome_arquivo, 'w') as file:
        json.dump(dados_exist, file, indent=4)

    upload_blob(nome_arquivo, nome_arquivo, pasta)
# Exemplo de uso:
# Suponha que você já tenha um DataFrame df

