from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def create_driver(headless=True):

    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless=new")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    chrome_driver_path = "/usr/local/bin/chromedriver"
    
    if os.path.exists(chrome_driver_path):
        service = Service(executable_path=chrome_driver_path)
        print(f"Используем chromedriver из: {chrome_driver_path}")
    else:
        raise FileNotFoundError(f"ChromeDriver не найден по пути: {chrome_driver_path}")
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Ошибка при создании драйвера: {e}")
        raise