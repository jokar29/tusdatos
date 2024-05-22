import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

url = "https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros"

dic = {
    "demandante": [],
    "fecha": [],
    "proceso": [],
    "accion": []
}

def export_csv(data):
    """
     Exportar data a csv
    """
    df = pd.DataFrame(data)
    df.to_csv("casos.csv", index=False)


"""
opciones de navegacion
"""

opts = Options()
opts.add_argument('--start-maximized')

def procesar_numero(driver2, numero):

    driver2.find_element(By.CSS_SELECTOR,'input#mat-input-1').send_keys(numero)
    time.sleep(5)
    driver2.find_element(By.CSS_SELECTOR,'button.boton-buscar.mdc-button.mdc-button--raised.mat-mdc-raised-button.mat-accent.mat-mdc-button-base').click()
    time.sleep(5)

    data = driver2.find_elements(By.XPATH, '//div[contains(@class, "causa-individual")]')

    for dato in data:
        fecha = dato.find_element(By.XPATH, './/div[@class="fecha"]').text
        procesos = dato.find_element(By.XPATH, './/div[@class="numero-proceso"]').text
        accion = dato.find_element(By.XPATH, './/div[@class="accion-infraccion"]').text
        dic["demandante"].append(numero)
        dic["fecha"].append(fecha)
        dic["proceso"].append(procesos)
        dic["accion"].append(accion)
        time.sleep(5)
        driver2.find_element(By.XPATH, '//button[contains(@aria-label, "regresar")]').click()
        time.sleep(5)
    #     time.sleep(7)
    #     print(proceso.text)
    #     WebDriverWait(driver2, 3)
    #     print(causa.text)
    #     proceso_xpath = f'(.//a[contains(@aria-label, "proceso {causa.text}")])'
    #     causa.find_element(By.XPATH, proceso_xpath).click()
    #     time.sleep(5)
    #     driver2.find_element(By.XPATH, '//a[contains(@aria-label, "incidente")]').click()
    #     time.sleep(5)
    #     driver2.find_element(By.XPATH, '//button[contains(@aria-label, "regresar")]').click()
    #     time.sleep(7)
    #     driver2.find_element(By.XPATH, '//button[contains(@aria-label, "regresar")]').click()
    #     time.sleep(7)
        df = pd.DataFrame(dic)
        df.to_csv("casos.csv", index=False)
    # return dic
        print(dic)


if __name__ == "__main__":
    numeros = ['0968599020001', '0992339411001', '1791251237001']  # Lista de números

    # driver_path = 'path/to/chromedriver'
    driver2 = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )
    driver2.get(url)
    time.sleep(3)
    try:
        for numero in numeros:
            data = procesar_numero(driver2, numero)
            print(data)
            export_csv(data)

    finally:
        driver2.quit()
