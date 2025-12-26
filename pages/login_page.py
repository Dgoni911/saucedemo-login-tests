from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message = (By.CSS_SELECTOR, "[data-test='error']")
        self.inventory_container = (By.ID, "inventory_container")
        
    @allure.step("Открыть страницу логина")
    def open(self):
        self.driver.get("https://www.saucedemo.com/")
        return self
        
    @allure.step("Ввести имя пользователя: {username}")
    def enter_username(self, username):
        username_field = self.wait.until(
            EC.visibility_of_element_located(self.username_field)
        )
        username_field.clear()
        username_field.send_keys(username)
        return self
        
    @allure.step("Ввести пароль: {password}")
    def enter_password(self, password):
        password_field = self.wait.until(
            EC.visibility_of_element_located(self.password_field)
        )
        password_field.clear()
        password_field.send_keys(password)
        return self
        
    @allure.step("Нажать кнопку логина")
    def click_login(self):
        login_button = self.wait.until(
            EC.element_to_be_clickable(self.login_button)
        )
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
            error_element = self.wait.until(
                EC.visibility_of_element_located(self.error_message)
            )
            return error_element.text
        except:
            return None
            
    @allure.step("Проверить успешный логин")
    def is_inventory_page_displayed(self):
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.inventory_container)
            )
            return True
        except:
            return False
            
    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url