from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("У пользователя должен быть логин")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

# Создание таблицы пользователей или модели в Джанго
class User(AbstractBaseUser, PermissionsMixin):
    ADMINISTRATOR = 'администратор'
    MANAGER = 'менеджер'
    STUDENT = 'студент'
    TEACHER = 'преподаватель'
    ROLE_CHOICES = [
        (ADMINISTRATOR, 'администратор'),
        (MANAGER, 'менеджер'),
        (STUDENT, 'студент'),
        (TEACHER, 'преподаватель'),
    ]

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45,blank=False, unique=True)
    surname = models.CharField(max_length=45, blank=False, verbose_name="Фамилия")
    name = models.CharField(max_length=45, blank=False, verbose_name="Имя")
    patronymic = models.CharField(max_length=45, blank=True, verbose_name="Отчество")
    email = models.EmailField(max_length=45,  blank=False)
    role = models.CharField(max_length=13, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'accounts_user'
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=['surname', 'name', 'patronymic', 'email'],
                name='unique_info_UNIQUE'
            )
        ]
    def __str__(self):
        return (f'{self.id} | '
                f'{self.username}  | '
                f'{self.surname} | '
                f'{self.name} | '
                f'{self.patronymic} | '
                f'{self.email} | '
                f'{self.role}')


class Profile(models.Model):
    PROFILE_CHOICES = [
        ('ИИ и анализ данных', 'ИИ и анализ данных'),
        ('Корпоративный ИС', 'Корпоративный ИС'),
        ('Кибербезопасность ЦП', 'Кибербезопасность ЦП'),
        ('Игровая компьютерная индустрия', 'Игровая компьютерная индустрия'),
        ('Бизнес-аналитик 1С', 'Бизнес-аналитик 1С'),
        ('Цифровой дизайн и веб-разработка', 'Цифровой дизайн и веб-разработка'),
    ]  # Тип данных enum не поддерживается Django, его реализация сложнее, чем CharField+Choices

    id_profile = models.AutoField(primary_key=True)           # SERIAL
    name_of_profile = models.CharField(
        max_length=50,
        choices=PROFILE_CHOICES,
        unique=True,  # UNIQUE. Один и тот же предмет не должен повторяться
        blank=False
    )

    class Meta:
        db_table = 'profile'          # имя таблицы
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.name_of_profile


class Curriculum(models.Model):
    EDU_TYPE_CHOICES = [
        ('бакалавриат', 'бакалавриат'),
        ('магистратура', 'магистратура'),
        ('специалитет', 'специалитет'),
    ]

    id_curriculum = models.AutoField(primary_key=True)  # SERIAL PRIMARY KEY
    year_of_learning_start = models.SmallIntegerField(
        validators=[MinValueValidator(2000)]
    )
    num_of_semesters_of_study = models.SmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    type_of_higher_education = models.CharField(
        max_length=12,
        choices=EDU_TYPE_CHOICES
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.RESTRICT,
        db_column='id_profile'
    )

    class Meta:
        db_table = 'curriculum'
        # составной UNIQUE
        constraints = [
            models.UniqueConstraint(
                fields=['year_of_learning_start', 'num_of_semesters_of_study',
                        'type_of_higher_education', 'profile'],
                name='curriculum_year_num_type_profile_unique'
            )
        ]
        verbose_name = 'Учебный план'
        verbose_name_plural = 'Учебные планы'

    def __str__(self):
        return (f'{self.profile} | '
                f'{self.type_of_higher_education} | '
                f'{self.year_of_learning_start} | '
                f'{self.num_of_semesters_of_study} сем'
                )


class Subject(models.Model):
    id_subject = models.AutoField(primary_key=True)  # SERIAL PRIMARY KEY

    SUBJECT_CHOICES = [
        ('Автоматизация решения ОиРЗ в КИС', 'Автоматизация решения ОиРЗ в КИС'),
        ('Базы данных', 'Базы данных'),
        ('Алгоритмизация, программирование', 'Алгоритмизация, программирование'),
        ('Высокоуровневые методы программирования', 'Высокоуровневые методы программирования'),
    ]

    name_of_subject = models.CharField(
        max_length=100,
        choices=SUBJECT_CHOICES,
        unique=True   # нужно, чтобы не повторялись
    )

    class Meta:
        db_table = 'subjects'
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'

    def __str__(self):
        return self.name_of_subject


class LearningSubject(models.Model):
    id_learning_subjects = models.AutoField(primary_key=True)

    # связи ForeignKey
    subject = models.ForeignKey(
        Subject,
        on_delete=models.RESTRICT,
        db_column='id_subject'
    )
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.RESTRICT,
        db_column='id_curriculum'
    )

    semester_after_learning = models.SmallIntegerField(
        validators=[MinValueValidator(1)]  # семестр ≥ 1
    )

    class Meta:
        db_table = 'learning_subjects'
        constraints = [models.UniqueConstraint(fields=['subject',
                                               'curriculum', 'semester_after_learning'],
                                               name='curric_semes_subject_unique'
            )
        ]
        verbose_name = 'Изученный предмет'
        verbose_name_plural = 'Изученные предметы'

    def __str__(self):
        return f'{self.subject} - семестр изучения {self.semester_after_learning} | {self.curriculum} '


class Review(models.Model):
    SCORE_CHOICES = [
        ('Негативный',   'Негативный'),
        ('Нейтральный',  'Нейтральный'),
        ('Положительный','Положительный'),
    ]

    id_review = models.AutoField(primary_key=True)

    date_of_loading = models.DateField(auto_now_add=True)          # DATE NOT NULL

    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        limit_choices_to={'role__in': ['студент', 'менеджер']},
        db_column='id'
    )

    learning_subject = models.ForeignKey(
        LearningSubject,
        on_delete=models.RESTRICT,
        db_column='id_learning_subjects'
    )

    review = models.CharField(
        max_length=512,
        unique=True,
        validators=[MaxLengthValidator(512)]   # CHECK char_length(review) <= 512
    )

    score_of_review = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0)]  # примерный диапазон
    )

    name_of_score = models.CharField(
        max_length=13,
        choices=SCORE_CHOICES,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [models.UniqueConstraint(fields=['learning_subject',
                                               'user'], name='user_subj__unique'
            )
        ]

    def __str__(self):
        return f'Отзыв #{self.id_review} на дисциплину "{self.learning_subject}" от ({self.user})'


class StudentGroup(models.Model):
    id_student_group = models.AutoField(primary_key=True)

    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.RESTRICT,
        db_column='id_curriculum'
    )

    class Meta:
        db_table = 'student_group'
        unique_together = ('id_student_group', 'curriculum')
        verbose_name = 'Студенческая группа'
        verbose_name_plural = 'Студенческие группы'

    def __str__(self):
        return f'Группа {self.id_student_group} (уч. план {self.curriculum})'


class Student(models.Model):
    id_student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.RESTRICT,
        limit_choices_to={'role': 'студент'},
        db_column='id_student'
    )

    student_group = models.OneToOneField(
        StudentGroup,
        on_delete=models.RESTRICT,
        db_column='id_student_group'
    )

    class Meta:
        db_table = 'students'
        unique_together = ('id_student', 'student_group')
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return f'{self.id_student} – группа {self.student_group}'
