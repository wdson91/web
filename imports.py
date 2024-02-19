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
from salvardados import salvar_dados
import chromedriver_autoinstaller

from voupra.voupradisney.voupradisney import coletar_precos_voupra_disney
from voupra.vouprasea.vouprasea import coletar_precos_voupra_sea
from voupra.vouprauniversal.vouprauniversal import coletar_precos_voupra_universal
from insert_database import inserir_dados_no_banco


from ml.index_ml import main_ml
from voupra.index_voupra import main_voupra # Importando a função main do primeiro script
from vmz.index_vmz import main_vmz # Importando a função do segundo script

from vmz.vmzdisney.vmz_disney import coletar_precos_vmz
from vmz.vmzsea.vmzsea import coletar_precos_vmz_seaworld
from vmz.vmzuniversal.vmzuniversal import coletar_precos_vmz_universal


from ml.ml_universal.ml_universal import coletar_precos_ml_universal
from ml.mldisney.ml_disney import coletar_precos_ml_disney
from ml.mlsea.mlsea import coletar_precos_ml_seaworld

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
