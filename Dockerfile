# Use a imagem oficial do Python como base
FROM python:3.8

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos para o contêiner
COPY requirements.txt .

# Instale as dependências da aplicação
RUN pip install -r requirements.txt

# Copie todo o conteúdo do diretório local para o contêiner
COPY . .

# Comando para executar a aplicação Python
CMD ["python", "index.py"]
