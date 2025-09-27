# tests/test_smoke_urls.py
"""
Смоук-тесты маршрутов приложения accounts.
Проверяем:
  - корректность reverse() (генерация URL)
  - корректность resolve() (поиск view-функции по пути)
  - отсутствие 500-х ошибок при обращении к страницам
"""

from django.test import TestCase
from django.urls import reverse, resolve
from accounts import views


class AccountsUrlsSmokeTest(TestCase):
    """Проверяем, что маршруты accounts резолвятся и не 500-ят."""

    #  тесты reverse и resolve
    def test_login_url_resolves(self):
        """/accounts/login/ → login_view"""
        url = reverse('accounts:login')
        self.assertEqual(url, '/accounts/login/')
        self.assertEqual(resolve(url).func, views.login_view)

    def test_logout_url_resolves(self):
        """/accounts/logout/ → logout_view"""
        url = reverse('accounts:logout')
        self.assertEqual(url, '/accounts/logout/')
        self.assertEqual(resolve(url).func, views.logout_view)

    def test_role_redirect_url_resolves(self):
        """/accounts/ → role_redirect (главная после авторизации)"""
        url = reverse('accounts:role_redirect')
        self.assertEqual(url, '/accounts/')
        self.assertEqual(resolve(url).func, views.role_redirect)

    #  опционально – проверка статуса 200 (без авторизации)
    def test_login_page_returns_200(self):
        """Страница логина доступна анониму."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_page_returns_302(self):
        """Logout делает redirect на логин."""
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)