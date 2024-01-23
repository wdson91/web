from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import TimeoutException

def iniciar_navegador():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver


def aceitar_cookies(driver):
    try:
        botao_cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[2]/button'))
        )
        botao_cookies.click()
        print("Cookies aceitos.")
    except NoSuchElementException:
        print("Botão de cookies não encontrado.")
    except TimeoutException:
        print("Botão de cookies não disponível a tempo.")
        
def fechar_popups(driver):
    try:
        botao_fechar_selector = '.dinTargetFormCloseButtom'
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, botao_fechar_selector))
        ).click()
        print("Pop-up fechado.")
    except NoSuchElementException:
        print("Nenhum pop-up encontrado.")

def rolar_para_elemento(driver, elemento):
    driver.execute_script("arguments[0].scrollIntoView(true);", elemento)

def esperar_e_clicar_elemento(driver, elemento):
    try:
        rolar_para_elemento(driver, elemento)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(elemento)
        ).click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", elemento)

def coletar_valor_xpath(driver, xpath):
    try:
        elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return elemento.text
    except NoSuchElementException:
        print("Elemento não encontrado pelo XPath fornecido.")

driver = iniciar_navegador()
driver.get("https://www.vmzviagens.com.br/ingressos/orlando/walt-disney-orlando/ticket-disney-basico?mes=2024-23&dias=2")

time.sleep(5)
aceitar_cookies(driver)
fechar_popups(driver)

elementos = driver.find_elements(By.CLASS_NAME, 'fc-content')
for elemento in elementos:
    data = elemento.find_element(By.CLASS_NAME, 'fc-date').text
    if data == '31':
        esperar_e_clicar_elemento(driver, elemento)
        break

xpath = '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[3]/div/div[2]/div[2]/div/div/div[3]/div/p[5]/small[3]'
valor = coletar_valor_xpath(driver, xpath)
print("Valor do elemento:", valor)
time.sleep(50)

print("O navegador permanecerá aberto. Feche manualmente quando desejar.")
