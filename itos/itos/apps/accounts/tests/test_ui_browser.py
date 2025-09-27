"""
Интеграционный тест авторизации через реальный браузер (Selenium).
Проверяем:
  - страница логина открывается без ошибок
  - поля username/password доступны
  - успешный вход перенаправляет на главную (блог)
  - нет сообщений об ошибке после корректных данных
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model


class LoginBrowserTest(StaticLiveServerTestCase):
    """Тест авторизации в реальном браузере (headless Chrome)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Запускаем Chrome в headless-режиме (без GUI)
        options = Options()
        options.add_argument("--headless=new")  # современный headless
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)  # ожидание элементов до 10 сек

        # Создаём тестового пользователя
        user = get_user_model()
        user.objects.create_user(username='testuser', password='testpassword')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()  # закрываем браузер
        super().tearDownClass()

    def test_login_page(self):
        """Полный цикл: открыть страницу логина
        ввести данные
        войти
        проверить редирект.
        """
        # 1. Открываем страницу входа
        self.driver.get(f"{self.live_server_url}/accounts/login/")

        # 2. Проверяем заголовок страницы
        self.assertIn("Вход", self.driver.title)

        # 3. Находим поля ввода
        username_input = self.driver.find_element("name", "username")
        password_input = self.driver.find_element("name", "password")
        self.assertIsNotNone(username_input)
        self.assertIsNotNone(password_input)

        # 4. Вводим тестовые данные
        username_input.send_keys("testuser")
        password_input.send_keys("testpassword")

        # 5. Нажимаем кнопку входа
        login_button = self.driver.find_element("xpath", "//button[@type='submit']")
        login_button.click()

        # 6. Проверяем редирект на главную (блог)
        expected_url = f"{self.live_server_url}/blog/"
        current_url = self.driver.current_url.rstrip('/')  # убираем trailing slash
        self.assertEqual(current_url, expected_url.rstrip('/'))

        # 7. Убеждаемся, что нет сообщений об ошибке
        error_messages = self.driver.find_elements("css selector", ".alert-danger")
        self.assertEqual(len(error_messages), 0, "Сообщение об ошибке на странице авторизации")