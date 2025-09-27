# accounts/tests/test_login_form.py
"""
Unit-тест формы входа LoginForm.
Проверяем:
  - корректные данные проходят валидацию (is_valid=True)
  - можно расширить проверкой невалидных данных, help_text, ошибок и т.д.
"""

from django.test import TestCase
from accounts.forms import LoginForm


class FormUsabilityTest(TestCase):
    def test_login_form(self):
        """Форма принимает корректные логин/пароль."""
        form_data = {'username': 'testuser', 'password': 'testpassword'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())