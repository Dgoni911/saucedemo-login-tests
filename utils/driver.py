from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import allure

def create_driver(headless=True):
    """Создание и настройка драйвера Chrome"""
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
    
    # Проверяем Docker окружение
    is_docker = os.path.exists('/.dockerenv')
    
    if is_docker:
        # В Docker используем явный путь к chromedriver
        chrome_driver_path = "/usr/local/bin/chromedriver"
        if os.path.exists(chrome_driver_path):
            service = Service(executable_path=chrome_driver_path)
        else:
            # Если chromedriver не найден, попробуем использовать системный
            service = Service()
    else:
        # Локально используем стандартный путь
        service = Service()
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Ошибка при создании драйвера: {e}")
        raise