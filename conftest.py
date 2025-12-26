import pytest
import allure
from utils.driver import create_browser
import os

@pytest.fixture(scope="function")
def browser_manager():
    is_docker = os.path.exists('/.dockerenv')
    headless_mode = is_docker or os.getenv('HEADLESS', 'true').lower() == 'true'
    
    manager, page = create_browser(headless=headless_mode)
    
    yield manager, page
    
    manager.stop()

@pytest.fixture(scope="function")
def page(browser_manager):
    manager, page_instance = browser_manager
    return page_instance

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            browser_manager = item.funcargs.get('browser_manager')
            if browser_manager:
                manager, page = browser_manager
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                
                html = page.content()
                allure.attach(
                    html,
                    name="page_html",
                    attachment_type=allure.attachment_type.HTML
                )
        except Exception as e:
            print(f"Failed to capture screenshot or HTML: {e}")