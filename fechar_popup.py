# fechar_popup.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fechar_popup():
    chrome_options = Options()
    chrome_driver_path = '/caminho/para/chromedriver'
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    
    driver.get("https://www.exemplo.com")

    while True:
        try:
            poup_02 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "dismiss-button")))
            poup_02.click()
            print("Popup fechado")
        except Exception as e:
            print(f"Erro ao tentar fechar popup: {e}")
        time.sleep(5)

if __name__ == "__main__":
    fechar_popup()
