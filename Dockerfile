# Use uma imagem base que inclua o Python e o navegador de sua escolha
# Neste exemplo, usamos a imagem oficial do Python 3.8 com o Chrome
FROM python:3.8-slim-buster

# Instale as dependências necessárias
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Baixe e instale o Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN apt-get install -f -y

# Baixe e instale o ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/<versão_do_chromedriver>/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /usr/local/bin
RUN rm chromedriver_linux64.zip

# Defina a pasta de trabalho no contêiner
WORKDIR /app

# Instale as dependências Python necessárias
RUN pip install selenium

# Copie seu código Python para o contêiner
COPY . .

# Comando para executar o código Python quando o contêiner for iniciado
CMD ["python", "inde.py"]
