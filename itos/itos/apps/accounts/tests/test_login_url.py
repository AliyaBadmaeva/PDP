# accounts/tests/test_login_url.py
"""
Простой smoke: URL резолвится и возвращает 200.
"""

from django.test import TestCase
from django.urls import reverse


class URLUsabilityTest(TestCase):
    def test_login_url(self):
        """/accounts/login/ доступен и возвращает 200."""
        url = reverse('accounts:login')
        self.assertEqual(url, '/accounts/login/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)