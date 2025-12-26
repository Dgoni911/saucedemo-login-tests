from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import allure

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
    
    if os.path.exists("/usr/local/bin/chromedriver"):
        service = Service(executable_path="/usr/local/bin/chromedriver")
        print(f"Используем chromedriver из: /usr/local/bin/chromedriver")
    else:
        service = Service()
        print("Используем стандартный chromedriver")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver