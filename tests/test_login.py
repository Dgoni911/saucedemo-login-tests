import pytest
import allure
from pages.login_page import LoginPage
import time

@allure.feature("Авторизация пользователя")
@allure.story("Проверка различных сценариев авторизации")
class TestLogin:
    
    @allure.title("TC-1: Успешная авторизация с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("positive", "smoke")
    def test_successful_login(self, page):
        login_page = LoginPage(page)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
            
        with allure.step("2. Проверить элементы страницы логина"):
            assert login_page.is_element_present("#user-name"), "Поле username не найдено"
            assert login_page.is_element_present("#password"), "Поле password не найдено"
            assert login_page.is_element_present("#login-button"), "Кнопка login не найдена"
            
        with allure.step("3. Выполнить вход с валидными данными"):
            login_page.login("standard_user", "secret_sauce")
            
        with allure.step("4. Проверить успешную авторизацию"):
            assert login_page.is_inventory_page_displayed(), \
                "Страница инвентаря не отображается после успешного логина"
            
        with allure.step("5. Проверить URL после логина"):
            current_url = login_page.get_current_url()
            assert "inventory" in current_url.lower(), \
                f"Неверный URL после логина: {current_url}. Ожидается 'inventory' в URL"
                
        with allure.step("6. Проверить наличие элементов на странице инвентаря"):
            assert login_page.is_element_present(".inventory_list"), "Список товаров не отображается"
    
    @allure.title("TC-2: Авторизация с неверным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative")
    def test_login_with_wrong_password(self, page):
        login_page = LoginPage(page)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
            
        with allure.step("2. Выполнить вход с неверным паролем"):
            login_page.login("standard_user", "wrong_password")
            
        with allure.step("3. Проверить сообщение об ошибке"):
            error_message = login_page.get_error_message()
            assert error_message is not None, "Сообщение об ошибке не отображается"
            assert "Epic sadface: Username and password do not match" in error_message, \
                f"Неверное сообщение об ошибке: {error_message}"
                
        with allure.step("4. Проверить что остались на странице логина"):
            current_url = login_page.get_current_url()
            assert "saucedemo.com" in current_url, \
                f"Ожидалась страница логина, получен URL: {current_url}"
                
        with allure.step("5. Проверить что поля логина все еще доступны"):
            assert login_page.is_element_present("#user-name"), "Поле username пропало"
            assert login_page.is_element_present("#password"), "Поле password пропало"
    
    @allure.title("TC-3: Авторизация заблокированного пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative")
    def test_locked_out_user_login(self, page):
        login_page = LoginPage(page)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
            
        with allure.step("2. Попытка логина заблокированным пользователем"):
            login_page.login("locked_out_user", "secret_sauce")
            
        with allure.step("3. Проверить сообщение о блокировке"):
            error_message = login_page.get_error_message()
            assert error_message is not None, "Сообщение об ошибке не отображается"
            assert "Epic sadface: Sorry, this user has been locked out." in error_message, \
                f"Неверное сообщение об ошибке: {error_message}"
                
        with allure.step("4. Проверить что кнопка логина доступна для повторной попытки"):
            assert login_page.is_element_present("#login-button"), \
                "Кнопка логина недоступна для повторной попытки"
    
    @allure.title("TC-4: Авторизация с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "validation")
    def test_login_with_empty_fields(self, page):
        login_page = LoginPage(page)
        
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
            
        with allure.step("2. Нажать кнопку логина без заполнения полей"):
            login_page.click_login()
            
        with allure.step("3. Проверить сообщение об ошибке"):
            error_message = login_page.get_error_message()
            assert error_message is not None, "Сообщение об ошибке не отображается"
            assert "Epic sadface: Username is required" in error_message, \
                f"Неверное сообщение об ошибке: {error_message}"
                
        with allure.step("4. Проверить подсветку полей с ошибкой"):
            error_fields = page.locator(".error")
            assert error_fields.count() > 0, "Поля с ошибкой не подсвечены"
    
    @allure.title("TC-5: Авторизация пользователя performance_glitch_user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("positive", "performance")
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
            assert "inventory" in current_url.lower(), \
                f"Неверный URL после логина: {current_url}"
                
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        with allure.step(f"5. Замер времени загрузки: {elapsed_time:.2f} секунд"):
            allure.attach(
                f"Общее время выполнения логина: {elapsed_time:.2f} секунд\n"
                f"Старт: {time.ctime(start_time)}\n"
                f"Завершение: {time.ctime(end_time)}",
                name="Время выполнения",
                attachment_type=allure.attachment_type.TEXT
            )
            
            print(f"Время выполнения логина performance_glitch_user: {elapsed_time:.2f} секунд")
            
            assert elapsed_time < 30, f"Логин занял слишком много времени: {elapsed_time:.2f} секунд"