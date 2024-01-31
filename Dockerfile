# Use a imagem oficial do Python como base
FROM python:3.8

# Define a pasta de trabalho no contêiner
WORKDIR /app

# Instale as dependências do Python
RUN pip install --upgrade pip
RUN pip install aiohttp pandas selenium webdriver_manager
RUN pip install psycopg2-binary
# Copie o seu código fonte para o contêiner
COPY . .

# Execute o seu código Python quando o contêiner for iniciado
CMD ["python", "index.py"]
