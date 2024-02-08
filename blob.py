from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Substitua pelos seus detalhes de conexão
def upload_blob(caminho_arquivo_json,nome_arquivo_json,pasta):
    
    connect_str = "DefaultEndpointsProtocol=https;AccountName=sdarq;AccountKey=1WFQXUd7f2vQwRLa2EZod7EtrtyE7HmlKZwBWfby5EuAPy2TvFgM/XSfyG5SzqxIQriIYLpqgMNrEANpCIP0cA==;EndpointSuffix=core.windows.net"
    container_name = f'imagens/Automacao_python/{pasta}'
    file_path = caminho_arquivo_json
    blob_name = nome_arquivo_json

    # Criar o BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Obter o ContainerClient
    container_client = blob_service_client.get_container_client(container_name)

    # Criar o blob client
    blob_client = container_client.get_blob_client(blob_name)

    # Carregar o arquivo e enviar para o Blob Storage
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
