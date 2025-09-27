# accounts/tests/test_ui_render.py
from django.test import TestCase
from django.urls import reverse


class UiRenderTest(TestCase):
    """Без браузера: проверяем, что нужные блоки есть в HTML."""

    def test_login_page_contains_form(self):
        """На странице логина должен быть тег <form> и поля username/password."""
        response = self.client.get(reverse('accounts:login'))

        # есть форма
        self.assertContains(response, '<form')
        # есть поле логина
        self.assertContains(response, 'name="username"')
        # есть поле пароля
        self.assertContains(response, 'name="password"')