# SauceDemo Automation Testing

Проект для автоматизации тестирования логина на сайте SauceDemo.

## Описание
Проект содержит автоматизированные тесты для проверки функциональности логина на сайте https://www.saucedemo.com/.

## Тестовые сценарии
1. Успешный логин (standard_user / secret_sauce)
2. Логин с неверным паролем
3. Логин заблокированного пользователя (locked_out_user)
4. Логин с пустыми полями
5. Логин пользователем performance_glitch_user

## Требования
- Python 3.10+
- Docker (опционально)

## Установка

pip install -r requirements.txt

# Запуск всех тестов
python -m pytest

# Запуск с генерацией Allure отчетов
pytest --alluredir=allure-results

# Просмотр отчета Allure
allure serve allure-results

# Сборка образа
docker build -t saucedemo-tests .

# Запуск тестов в контейнере
docker run saucedemo-tests"# Test update" 
