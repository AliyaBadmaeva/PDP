# accounts/tests/test_login_template.py
"""
Проверяем, что шаблон login.html:
  - используется корректно
  - содержит ожидаемые русскоязычные подписи
"""

from django.test import TestCase
from django.urls import reverse


class TemplateUsabilityTest(TestCase):
    def test_login_template(self):
        """Шаблон login.html отдаёт 200 и содержит русские подписи полей."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        # проверяем человечески-понятные подписи
        self.assertContains(response, 'Логин')
        self.assertContains(response, 'Пароль')
        self.assertContains(response, 'Вход')