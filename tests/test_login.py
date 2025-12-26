import pytest
import allure
from pages.login_page import LoginPage
import time

@allure.feature("Авторизация пользователя")
@allure.story("Проверка различных сценариев авторизации")
class TestLogin:
    
    @allure.title("Успешная авторизация с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, driver):
        login_page = LoginPage(driver)
        
        with allure.step("Открыть страницу логина и выполнить вход"):
            login_page.open().login("standard_user", "secret_sauce")
            
        with allure.step("Проверить успешную авторизацию"):
            assert login_page.is_inventory_page_displayed(), \
                "Страница инвентаря не отображается после успешного логина"
            
        with allure.step("Проверить URL после логина"):
            assert "inventory" in login_page.get_current_url().lower(), \
                f"Неверный URL после логина: {login_page.get_current_url()}"
    
    @allure.title("Авторизация с неверным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_wrong_password(self, driver):
        login_page = LoginPage(driver)
        
        with allure.step("Открыть страницу логина и ввести неверный пароль"):
            login_page.open().login("standard_user", "wrong_password")
            
        with allure.step("Проверить сообщение об ошибке"):
            error_message = login_page.get_error_message()
            assert error_message is not None, "Сообщение об ошибке не отображается"
            assert "Epic sadface: Username and password do not match" in error_message, \
                f"Неверное сообщение об ошибке: {error_message}"
                
        with allure.step("Проверить что остались на странице логина"):
            assert "saucedemo.com" in login_page.get_current_url(), \
                "Остались на странице логина"
    
    @allure.title("Авторизация заблокированного пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_locked_out_user_login(self, driver):
        login_page = LoginPage(driver)
        
        with allure.step("Попытка логина заблокированным пользователем"):
            login_page.open().login("locked_out_user", "secret_sauce")
            
        with allure.step("Проверить сообщение о блокировке"):
            error_message = login_page.get_error_message()
            assert error_message is not None, "Сообщение об ошибке не отображается"
            assert "Epic sadface: Sorry, this user has been locked out." in error_message, \
                f"Неверное сообщение об ошибке: {error_message}"
    
    @allure.title("Авторизация с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_empty_fields(self, driver):
        login_page = LoginPage(driver)
        
        with allure.step("Открыть страницу логина и нажать кнопку без заполнения полей"):
            login_page.open().click_login()
            
        with allure.step("Проверить сообщение об ошибке"):
            error_message = login_page.get_error_message()
            assert error_message is not None, "Сообщение об ошибке не отображается"
            assert "Epic sadface: Username is required" in error_message, \
                f"Неверное сообщение об ошибке: {error_message}"
    
    @allure.title("Авторизация пользователя performance_glitch_user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_performance_glitch_user_login(self, driver):
        login_page = LoginPage(driver)
        start_time = time.time()
        
        with allure.step("Логин пользователем performance_glitch_user"):
            login_page.open().login("performance_glitch_user", "secret_sauce")
            
        with allure.step("Проверить что страница загрузилась несмотря на задержки"):
            assert login_page.is_inventory_page_displayed(), \
                "Страница инвентаря не отображается после логина performance_glitch_user"
            
        with allure.step("Проверить URL после логина"):
            assert "inventory" in login_page.get_current_url().lower(), \
                f"Неверный URL после логина: {login_page.get_current_url()}"
                
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        with allure.step(f"Замер времени загрузки: {elapsed_time:.2f} секунд"):
            allure.attach(
                f"Время выполнения логина: {elapsed_time:.2f} секунд",
                name="Время выполнения",
                attachment_type=allure.attachment_type.TEXT
            )
            
            print(f"Время выполнения логина performance_glitch_user: {elapsed_time:.2f} секунд")