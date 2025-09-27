# apps/accounts/tests/test_critical_path.py
"""
Критический-путь (smoke) тесты приложения accounts.
Проверяем:
  - главные маршруты не 500-ят
  - главная view отдаёт 200/302
  - модель Review создаётся без ошибок
  - уникальные/внешние ключи работают
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Review, LearningSubject, Subject, Curriculum, Profile

User = get_user_model()


class CriticalPathSmokeTest(TestCase):
    """Критический путь: URLs + главные views + создание объекта."""

    # разрешаем обращения к БД
    databases = '__all__'
    allow_database_queries = True

    @classmethod
    def setUpTestData(cls):
        """Создаём минимальный набор справочников для всех тестов."""
        # профиль подготовки
        cls.profile = Profile.objects.create(name_of_profile="Test Profile")

        # учебный план
        cls.curriculum = Curriculum.objects.create(
            year_of_learning_start=2023,
            num_of_semesters_of_study=8,
            type_of_higher_education="бакалавриат",
            profile=cls.profile
        )

        # дисциплина
        cls.subject = Subject.objects.create(name_of_subject="Math")

        # связь «дисциплина-семестр» (важно: передаём объект, а не id)
        cls.ls = LearningSubject.objects.create(
            subject=cls.subject,
            curriculum=cls.curriculum,   # ← объект, не 1
            semester_after_learning=1
        )

    #  URLS: главные страницы не 500-ят
    def test_login_page_resolves(self):
        """/accounts/login/ доступна и не падает с 500."""
        url = reverse('accounts:login')
        response = self.client.get(url)
        # может быть 200 (форма) или 302 (редирект), но не 500
        self.assertIn(response.status_code, (200, 302))

    def test_root_redirect_resolves(self):
        """Корень приложения /accounts/ не падает."""
        response = self.client.get(reverse('accounts:role_redirect'))
        self.assertIn(response.status_code, (200, 302))

    #  Главная view: smoke-режим
    def test_dashboard_get_no_crash(self):
        """Главная дашборд-страница не выдаёт 500."""
        response = self.client.get('/accounts/')  # корень приложения
        self.assertNotEqual(response.status_code, 500)

    #  Модель Review: объект создаётся
    def test_review_can_be_created(self):
        """Модель Review создаётся без ошибок, внешние ключи корректны."""
        user = User.objects.create_user(
            username='cp',
            email='cp@test.local',
            password='pass'
        )
        review = Review.objects.create(
            user=user,
            learning_subject=self.ls,
            review='cp test',
            score_of_review=1.0,
            name_of_score='Neutral'
        )
        self.assertEqual(review.name_of_score, 'Neutral')