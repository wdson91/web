# Use a imagem oficial do Python como base
FROM python:3.8

# Define a pasta de trabalho no contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install -r requirements.txt

# Instale o driver do Chrome usando o webdriver_manager
RUN pip install webdriver_manager

# Copie o seu código fonte para o contêiner
COPY index.py .

# Execute o seu código Python quando o contêiner for iniciado
CMD ["python", "index.py"]
