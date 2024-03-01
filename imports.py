import asyncio
import os
import sys
import time
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import logging
from bs4 import BeautifulSoup
import json
import threading
import logging
from salvardados import *
from urllib.parse import urlparse, parse_qs
import chromedriver_autoinstaller
import asyncio  # Importa o módulo asyncio para suporte a tarefas assíncronas
import schedule  # Importa o módulo schedule para agendar tarefas
from datetime import datetime  # Importa a classe datetime do módulo datetime
import pytz  # Importa o módulo pytz para lidar com fusos horários
from selenium.common.exceptions import NoSuchElementException


from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs

import os

def get_directories():
    """
    Retorna uma tupla com os caminhos para o diretório atual, pai e avô do arquivo.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    grandparent_dir = os.path.dirname(parent_dir)

    return current_dir, parent_dir, grandparent_dir


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


#VMZ DISNEY 2 A 5 DIAS
nome_pacotes = {
        2: "2 Dias - Disney World Basico",
        3: "3 Dias - Disney World Basico",
        4: "4 Dias - Disney World Basico",
        5: "5 Dias - Disney World Basico"
    }

dias_para_processar = [2, 3, 4, 5]