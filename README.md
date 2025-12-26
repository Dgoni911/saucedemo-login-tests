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

1. Клонировать репозиторий:
```bash
git clone https://github.com/yourusername/saucedemo-automation.git
cd saucedemo-automation