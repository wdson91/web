import asyncio
#import pandas as pd
import logging
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import os
import geckodriver_autoinstaller
import sys
import time
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_pai = os.path.dirname(diretorio_atual)
diretorio_avo = os.path.dirname(diretorio_pai)

sys.path.insert(0, diretorio_avo)
import undetected_chromedriver as uc

my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
options = uc.Options()
options.add_argument("proxy-server=186.215.247.71:3128")
# Set up Chrome options




async def coletar_precos_ml_universal():
    #driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    uc.TARGET_VERSION = 85  
    driver = uc.Chrome(options=options)
    dados = []
    wait = WebDriverWait(driver, 5)
    days_to_add = [5, 10, 20, 47, 64, 126]
    url = f"https://www.decolar.com/atracoes-turisticas/d-DY_ORL/ingressos+para+walt+disney+world+resort-orlando?from=nav&distribution=1&modalityId=ANNUAL-MK-2024"
    driver.get(url)
    driver.save_screenshot("screenshot.png")
            
    time.sleep(500)
    

if __name__ == '__main__':
    asyncio.run(coletar_precos_ml_universal())
