import pytest
import allure
from selenium import webdriver
from utils.driver import create_driver
import os

@pytest.fixture(scope="function")
def driver():
    is_docker = os.path.exists('/.dockerenv')
    headless_mode = is_docker or os.getenv('HEADLESS', 'true').lower() == 'true'
    
    driver_instance = create_driver(headless=headless_mode)
    
    if not headless_mode:
        driver_instance.maximize_window()
    
    yield driver_instance
    
    driver_instance.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs.get('driver')
            if driver:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")