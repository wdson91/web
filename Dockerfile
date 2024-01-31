# Use a imagem oficial do Python como base
FROM python:3.8

# Define a pasta de trabalho no contêiner
WORKDIR /app

# Instale as dependências do Python
RUN pip install --upgrade pip
RUN pip install aiohttp pandas selenium webdriver_manager
RUN pip install psycopg2-binary
# Instale o Google Chrome
RUN apt-get update && apt-get install -y wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb

# Instale o Chrome WebDriver usando webdriver-manager
RUN webdriver-manager update

# Copie todo o conteúdo do diretório atual para o contêiner
COPY . .

# Execute o seu código Python quando o contêiner for iniciado
CMD ["python", "index.py"]
