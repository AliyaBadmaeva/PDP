# tests/test_models_smoke.py
"""
Смоук-тесты для всех кастомных моделей приложения accounts.
Проверяем:
  - создание объектов
  - уникальные ограничения
  - валидаторы полей
  - корректность строкового представления
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from accounts.models import (
    User, Profile, Curriculum, Subject, LearningSubject,
    Review, StudentGroup, Student
)

User = get_user_model()


class TestModelsSmoke(TestCase):
    """Быстрая проверка всех моделей и связей."""

    @classmethod
    def setUpTestData(cls):
        """Создаём общие объекты один раз для всего класса."""
        # справочники
        cls.profile = Profile.objects.create(name_of_profile="ИИ и анализ данных")
        cls.curriculum = Curriculum.objects.create(
            year_of_learning_start=2023,
            num_of_semesters_of_study=8,
            type_of_higher_education="бакалавриат",
            profile=cls.profile
        )
        cls.subject = Subject.objects.create(name_of_subject="Базы данных")
        cls.learning_subject = LearningSubject.objects.create(
            subject=cls.subject,
            curriculum=cls.curriculum,
            semester_after_learning=3
        )
        cls.student_group = StudentGroup.objects.create(curriculum=cls.curriculum)

        # пользователь и студент
        cls.user_student = User.objects.create(
            username="student1",
            surname="Иванов",
            name="Иван",
            patronymic="Иванович",
            email="stu@test.local",
            role=User.STUDENT
        )
        cls.student = Student.objects.create(id_student=cls.user_student,
                                             student_group=cls.student_group)

        # один отзыв (будет использоваться в тестах на уникальность)
        cls.review = Review.objects.create(
            user=cls.user_student,
            learning_subject=cls.learning_subject,
            review="Первый отзыв",
            score_of_review=1.0,
            name_of_score="Нейтральный"
        )

    #  тесты
    def test_user_create(self):
        """Проверяем, что __str__ содержит username."""
        self.assertIn("student1", str(self.user_student))

    def test_profile_unique(self):
        """Профиль должен быть уникальным по названию."""
        with self.assertRaises(ValidationError):
            Profile(name_of_profile=self.profile.name_of_profile).full_clean()

    def test_curriculum_unique_together(self):
        """Учебный план уникален по году + семестрам + уровню + профилю."""
        with self.assertRaises(ValidationError):
            Curriculum(
                year_of_learning_start=2023,
                num_of_semesters_of_study=8,
                type_of_higher_education="бакалавриат",
                profile=self.profile
            ).full_clean()

    def test_learning_subject_str(self):
        """Проверка строкового представления дисциплины-семестра."""
        expected = "Базы данных (отзыв доступен с семестра 3)"
        self.assertEqual(self.learning_subject.subject_with_semester(), expected)

    def test_review_create_by_student(self):
        """Создание отзыва вторым студентом на ту же дисциплину – должно пройти."""
        # вторая группа
        group2 = StudentGroup.objects.create(curriculum=self.curriculum)
        # второй пользователь и студент
        user2 = User.objects.create(
            username="student2",
            surname="Петров",
            name="Пётр",
            patronymic="Петрович",
            email="stu2@test.local",
            role=User.STUDENT
        )
        Student.objects.create(id_student=user2, student_group=group2)

        review = Review.objects.create(
            user=user2,
            learning_subject=self.learning_subject,
            review="Курс понравился, всё понятно",
            score_of_review=2.0,
            name_of_score="Положительный"
        )
        self.assertIsNotNone(review.pk)
        self.assertEqual(review.name_of_score, "Положительный")
        self.assertLessEqual(len(review.review), 512)

    def test_review_unique_per_user_subject(self):
        """Один пользователь может оставить только один отзыв на дисциплину."""
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                user=self.user_student,
                learning_subject=self.learning_subject,
                review="Второй отзыв"
            )

    def test_student_one_to_one(self):
        """Один пользователь = один студент (по первичному ключу)."""
        with self.assertRaises(ValidationError):
            Student(id_student=self.user_student,
                    student_group=self.student_group).full_clean()

    def test_review_text_max_length_validator(self):
        """Текст отзыва не должен превышать 512 символов."""
        with self.assertRaises(ValidationError):
            review = Review(
                user=self.user_student,
                learning_subject=self.learning_subject,
                review="X" * 513
            )
            review.full_clean()  # важно: без full_clean не проверяется длина

    def test_score_range_validator(self):
        """score_of_review должен быть в диапазоне 0.0–2.0."""
        with self.assertRaises(ValidationError):
            review = Review(
                user=self.user_student,
                learning_subject=self.learning_subject,
                review="Норм",
                score_of_review=3.0  # > 2.0
            )
            review.full_clean()