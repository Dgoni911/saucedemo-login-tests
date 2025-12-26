import allure

class LoginPage:
    def __init__(self, page):
        self.page = page
    
    @allure.step("Открыть страницу логина")
    def open(self):
        self.page.goto("https://www.saucedemo.com/")
        return self
    
    @allure.step("Ввести имя пользователя: {username}")
    def enter_username(self, username):
        self.page.locator("#user-name").fill(username)
        return self
    
    @allure.step("Ввести пароль: {password}")
    def enter_password(self, password):
        self.page.locator("#password").fill(password)
        return self
    
    @allure.step("Нажать кнопку логина")
    def click_login(self):
        self.page.locator("#login-button").click()
        return self
    
    @allure.step("Выполнить логин с username={username}, password={password}")
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
            self.page.wait_for_selector("#inventory_container", timeout=10000)
            return True
        except:
            return False
    
    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.page.url
    
    @allure.step("Ожидать загрузки элемента: {selector}")
    def wait_for_element(self, selector, timeout=10000):
        self.page.wait_for_selector(selector, timeout=timeout)
        return self