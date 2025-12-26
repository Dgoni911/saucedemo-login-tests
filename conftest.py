import pytest
import allure

@pytest.fixture(scope="function")
def page(browser):
    """Фикстура для создания новой страницы"""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080}
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="session")
def browser():
    """Фикстура для создания браузера"""
    # Импортируем здесь, чтобы избежать ошибок импорта
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        pytest.skip(f"Playwright не установлен: {e}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--window-size=1920,1080"
            ]
        )
        yield browser
        browser.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            page = item.funcargs.get('page')
            if page:
                allure.attach(
                    page.screenshot(full_page=True),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")