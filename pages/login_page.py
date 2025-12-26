from playwright.sync_api import Page, expect
import allure
import time

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 10000
        
    @allure.step("Открыть страницу логина SauceDemo")
    def open(self):
        self.page.goto("https://www.saucedemo.com/", wait_until="domcontentloaded")
        self.page.wait_for_load_state("networkidle")
        return self
        
    @allure.step("Ввести имя пользователя: {username}")
    def enter_username(self, username):
        username_field = self.page.locator("#user-name")
        username_field.wait_for(state="visible", timeout=self.timeout)
        username_field.fill("")
        username_field.fill(username)
        return self
        
    @allure.step("Ввести пароль: {password}")
    def enter_password(self, password):
        password_field = self.page.locator("#password")
        password_field.wait_for(state="visible", timeout=self.timeout)
        password_field.fill("")
        password_field.fill(password)
        return self
        
    @allure.step("Нажать кнопку логина")
    def click_login(self):
        login_button = self.page.locator("#login-button")
        login_button.wait_for(state="visible", timeout=self.timeout)
        login_button.click()
        return self
        
    @allure.step("Выполнить полный логин с username={username}, password={password}")
    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
        
    @allure.step("Получить текст ошибки")
    def get_error_message(self):
        try:
            error_element = self.page.locator("[data-test='error']")
            error_element.wait_for(state="visible", timeout=5000)
            return error_element.text_content()
        except:
            return None
            
    @allure.step("Проверить успешный логин")
    def is_inventory_page_displayed(self):
        try:
            self.page.wait_for_selector("#inventory_container, .inventory_list, #react-burger-menu-btn", 
                                      state="visible", timeout=15000)
            return True
        except:
            return False
            
    @allure.step("Проверить текущий URL")
    def get_current_url(self):
        return self.page.url
        
    @allure.step("Проверить наличие элемента на странице")
    def is_element_present(self, selector, timeout=5000):
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except:
            return False
            
    @allure.step("Сделать паузу на {seconds} секунд")
    def wait(self, seconds):
        time.sleep(seconds)
        return self