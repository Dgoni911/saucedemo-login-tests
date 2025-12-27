import pytest
import allure
from pages.login_page import LoginPage
import time

@allure.feature("Авторизация пользователя")
@allure.story("Проверка различных сценариев авторизации")
class TestLogin:
    
    @allure.title("TC-1: Успешная авторизация с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, page):
        login_page = LoginPage(page)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
        
        with allure.step("2. Выполнить вход с валидными данными"):
            login_page.login("standard_user", "secret_sauce")
        
        with allure.step("3. Проверить успешную авторизацию"):
            assert login_page.is_inventory_page_displayed(), \
                "Страница инвентаря не отображается после успешного логина"
        
        with allure.step("4. Проверить URL после логина"):
            current_url = login_page.get_current_url()
            assert "inventory" in current_url, \
                f"Неверный URL после логина: {current_url}"
    
    @allure.title("TC-2: Авторизация с неверным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_wrong_password(self, page):
        login_page = LoginPage(page)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
        
        with allure.step("2. Выполнить вход с неверным паролем"):
            login_page.login("standard_user", "wrong_password")
        
        with allure.step("3. Проверить сообщение об ошибке"):
            error_message = login_page.get_error_message()
            assert error_message is not None, "Сообщение об ошибке не отображается"
            assert "Username and password do not match" in error_message, \
                f"Неверное сообщение об ошибке: {error_message}"
    
    @allure.title("TC-3: Авторизация заблокированного пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_locked_out_user_login(self, page):
        login_page = LoginPage(page)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
        
        with allure.step("2. Попытка логина заблокированным пользователем"):
            login_page.login("locked_out_user", "secret_sauce")
        
        with allure.step("3. Проверить сообщение о блокировке"):
            error_message = login_page.get_error_message()
            assert error_message is not None, "Сообщение об ошибке не отображается"
            assert "Sorry, this user has been locked out." in error_message, \
                f"Неверное сообщение об ошибке: {error_message}"
    
    @allure.title("TC-4: Авторизация с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_empty_fields(self, page):
        login_page = LoginPage(page)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
        
        with allure.step("2. Нажать кнопку логина без заполнения полей"):
            login_page.click_login()
        
        with allure.step("3. Проверить сообщение об ошибке"):
            error_message = login_page.get_error_message()
            assert error_message is not None, "Сообщение об ошибке не отображается"
            assert "Username is required" in error_message, \
                f"Неверное сообщение об ошибке: {error_message}"
    
    @allure.title("TC-5: Авторизация пользователя performance_glitch_user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_performance_glitch_user_login(self, page):
        login_page = LoginPage(page)
        start_time = time.time()
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
        
        with allure.step("2. Логин пользователем performance_glitch_user"):
            login_page.login("performance_glitch_user", "secret_sauce")
        
        with allure.step("3. Проверить что страница загрузилась несмотря на задержки"):
            assert login_page.is_inventory_page_displayed(), \
                "Страница инвентаря не отображается после логина performance_glitch_user"
        
        with allure.step("4. Проверить URL после логина"):
            current_url = login_page.get_current_url()
            assert "inventory" in current_url, \
                f"Неверный URL после логина: {current_url}"
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        with allure.step(f"5. Замер времени загрузки: {elapsed_time:.2f} секунд"):
            allure.attach(
                f"Время выполнения логина: {elapsed_time:.2f} секунд",
                name="Время выполнения",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert elapsed_time < 30, f"Логин занял слишком много времени: {elapsed_time:.2f} секунд"