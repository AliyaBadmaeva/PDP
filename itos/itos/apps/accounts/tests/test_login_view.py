# accounts/tests/test_login_view.py
"""
Тест view-функции входа:
  - страница отдаёт 200
  - при корректных данных происходит redirect на главную
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class ViewUsabilityTest(TestCase):
    def setUp(self):
        """Создаём тестового пользователя для авторизации."""
        User = get_user_model()
        User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view(self):
        """GET – форма, POST – успешный вход и редирект на blog:main."""
        # проверяем, что форма открывается
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

        # отправляем корректные данные
        response = self.client.post(
            reverse('accounts:login'),
            {'username': 'testuser', 'password': 'testpassword'}
        )
        # после успешного входа должны попасть на главную (блог)
        self.assertRedirects(response, reverse('blog:main'))