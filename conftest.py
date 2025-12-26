import pytest
import allure
from selenium import webdriver
from utils.driver import create_driver
import os

@pytest.fixture(scope="function")
def driver():
    driver_instance = create_driver(headless=False)
    
    driver_instance.maximize_window()
    
    yield driver_instance
    
    driver_instance.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs['driver']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")