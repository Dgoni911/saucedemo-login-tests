import pytest
import allure
from utils.driver import create_driver

@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания и закрытия драйвера"""
    # В Docker всегда headless
    driver_instance = create_driver(headless=True)
    
    yield driver_instance
    
    # После теста
    driver_instance.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
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