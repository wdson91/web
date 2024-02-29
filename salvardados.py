import os
import json
from datetime import datetime
import pytz
import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Substitua pelos seus detalhes de conexão
connect_str = "DefaultEndpointsProtocol=https;AccountName=sdarq;AccountKey=1WFQXUd7f2vQwRLa2EZod7EtrtyE7HmlKZwBWfby5EuAPy2TvFgM/XSfyG5SzqxIQriIYLpqgMNrEANpCIP0cA==;EndpointSuffix=core.windows.net"
#container_name = f'imagens/Automacao_python/{pasta}'

# Função para verificar se o arquivo existe no Azure Blob Storage e baixá-lo
def baixar_blob_se_existir(nome_arquivo_json, pasta):
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(f'imagens/Automacao_python/{pasta}')
    blob_client = container_client.get_blob_client(nome_arquivo_json)

    if blob_client.exists():
        with open(nome_arquivo_json, "wb") as download_file:
            print(f"Arquivo {nome_arquivo_json} baixado com sucesso.")
            return download_file.write(blob_client.download_blob().readall())
        
    else:
        print(f"Arquivo {nome_arquivo_json} não existe no Blob Storage.")
    
# Função para fazer upload do arquivo para o Azure Blob Storage
def upload_blob(caminho_arquivo_json, nome_arquivo_json, pasta):
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(f'imagens/Automacao_python/{pasta}')
    blob_client = container_client.get_blob_client(nome_arquivo_json)

    with open(caminho_arquivo_json, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Arquivo {nome_arquivo_json} enviado com sucesso para {pasta}.")

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
def salvar_dados(df, nome_arquivo_json, pasta,hour):
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    data_hora_coleta = hour
    
    novos_dados = df.to_dict(orient='records')
    novo_registro = {'Hora_coleta': data_hora_coleta, 'Dados': novos_dados}

    # Baixar o arquivo JSON do Azure Blob Storage se ele existir
    baixar_blob_se_existir(nome_arquivo_json, pasta)

    # Carregar os dados existentes do arquivo JSON
    dados_exist = carregar_dados_json(nome_arquivo_json)

    # Adicionar o novo registro aos dados existentes
    dados_exist.append(novo_registro)

    # Salvar os dados no arquivo JSON
    with open(nome_arquivo_json, 'w') as file:
        json.dump(dados_exist, file, indent=4)

    # Fazer upload do arquivo atualizado para o Azure Blob Storage
    upload_blob(nome_arquivo_json, nome_arquivo_json, pasta)

def salvar_dados_margem(df, nome_arquivo_json, pasta, hour):
    # Converter o DataFrame para JSON
    json_data = df.to_json(orient='records')

    # Inicializar o cliente do serviço de Blob
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Referenciar o container no Blob Storage
    container_client = blob_service_client.get_container_client(f'imagens/Automacao_python/{pasta}')

    # Enviar o JSON para o Blob Storage com o nome desejado
    blob_client = container_client.get_blob_client(nome_arquivo_json)
    blob_client.upload_blob(json_data, overwrite=True)

    print(f"Arquivo {nome_arquivo_json} enviado com sucesso para {pasta}.")
