# Модели пользователей, учебных сущностей и отзывов
# Используется кастомная модель User и полноценная ролевая система
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.conf import settings

# Менеджер пользователей
class UserManager(BaseUserManager):
    """
    Создание пользователей и суперпользователей.
    USERNAME_FIELD = 'username'  - аутентификация по логину.
    """
    def create_user(self, username, password=None, **extra_fields):  # создание пользователя
        if not username:  # если логин не заполнен
            raise ValueError("У пользователя должен быть логин")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)    # хэшируем пароль
        user.save(using=self._db)  # сохраняем пользователя в БД
        return user

    def create_superuser(self, username, password=None, **extra_fields):  # создание суперпользователя
        extra_fields.setdefault('is_staff', True)  # является ли пользователь персоналом
        extra_fields.setdefault('is_superuser', True)  # является ли пользователь суперпользователем
        return self.create_user(username, password, **extra_fields)

# Создание таблицы пользователей или модели в Джанго - кастомная модель пользователя
class User(AbstractBaseUser, PermissionsMixin):
    """Расширенная модель пользователя с ролями:
    админ, менеджер, студент, преподаватель."""

    # роли пользовтателей
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

    id = models.AutoField(primary_key=True)  # первичный ключ
    # логин - макс длина 45, не может быть пустым, должен быть уникальным
    username = models.CharField(max_length=45,blank=False, unique=True)
    # фамилия - макс длина 45, не может быть пустым, выводится в БД как Фамилия
    surname = models.CharField(max_length=45, blank=False, verbose_name="Фамилия")
    # имя - макс длина 45, не может быть пустым, выводится в БД как Имя
    name = models.CharField(max_length=45, blank=False, verbose_name="Имя")
    # отчество - макс длина 45, может быть пустым, выводится в БД как Отчество
    patronymic = models.CharField(max_length=45, blank=True, verbose_name="Отчество")
    # emai - макс длина 45, не может быть пустым
    email = models.EmailField(max_length=45,  blank=False)
    # роль - макс длина 13, выбор одного из вариантов ролей
    role = models.CharField(max_length=13, choices=ROLE_CHOICES)
    # пользователь активен - по умолчанию - истина
    is_active = models.BooleanField(default=True)
    # пользователь является персоналом - по умолчанию - ложь
    is_staff = models.BooleanField(default=False)
    # дата присоединения к ИТОС - проставляется время создания пользователя
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()  # создаем объект класса

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # требуемые поля

    class Meta:
        # название таблицы в БД
        db_table = 'accounts_user'

        # Django управляет этой таблицей: создает при миграциях и удаляет при очистке БД
        managed = True
        # Уникальность ФИО+email
        constraints = [
            models.UniqueConstraint(
                fields=['surname', 'name', 'patronymic', 'email'],
                name='unique_info_UNIQUE'
            )
        ]

    # вывод полей в БД
    def __str__(self):
        return (f'{self.id} | '
                f'{self.username}  | '
                f'{self.surname} | '
                f'{self.name} | '
                f'{self.patronymic} | '
                f'{self.email} | '
                f'{self.role}')


# создание класса профили обучение
class Profile(models.Model):
    """Направление подготовки (ИИ, ИБ, 1С и т.д.)."""
    PROFILE_CHOICES = [
        ('ИИ и анализ данных', 'ИИ и анализ данных'),
        ('Корпоративный ИС', 'Корпоративный ИС'),
        ('Кибербезопасность ЦП', 'Кибербезопасность ЦП'),
        ('Игровая компьютерная индустрия', 'Игровая компьютерная индустрия'),
        ('Бизнес-аналитик 1С', 'Бизнес-аналитик 1С'),
        ('Цифровой дизайн и веб-разработка', 'Цифровой дизайн и веб-разработка'),
    ]  # Тип данных enum не поддерживается Django, его реализация сложнее, чем CharField+Choices

    id_profile = models.AutoField(primary_key=True)           # SERIAL
    # наименование профиля - на выбор из PROFILE_CHOICES
    name_of_profile = models.CharField(
        max_length=50,  # макс. длина
        choices=PROFILE_CHOICES,
        unique=True,  # UNIQUE. Один и тот же предмет не должен повторяться
        blank=False  # не может быть пустым
    )

    class Meta:
        db_table = 'profile'          # имя таблицы
        verbose_name = 'Профиль'   # как будет показано в админке
        verbose_name_plural = 'Профили'  # множественное число названия таблицы

    def __str__(self):
        return self.name_of_profile

# Учебный план
class Curriculum(models.Model):
    """Учебный план: id, год старта, кол-во семестров, уровень, профиль."""
    EDU_TYPE_CHOICES = [
        ('бакалавриат', 'бакалавриат'),
        ('магистратура', 'магистратура'),
        ('специалитет', 'специалитет'),
    ]

    id_curriculum = models.AutoField(primary_key=True)  # SERIAL PRIMARY KEY
    # год начала обучения (мин. год = 2000)
    year_of_learning_start = models.SmallIntegerField(
        validators=[MinValueValidator(2000)]
    )
    # количество семестров обучения (мин. - 1)
    num_of_semesters_of_study = models.SmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    # тип высшего образования (выбираем из EDU_TYPE_CHOICES)
    type_of_higher_education = models.CharField(
        max_length=12,
        choices=EDU_TYPE_CHOICES
    )
    # профиль подготовки из таблицы (модели) Профиль - внешний ключ
    profile = models.ForeignKey(
        Profile,
        on_delete=models.RESTRICT,
        db_column='id_profile'
    )

    class Meta:
        db_table = 'curriculum'  # название в БД
        # составной UNIQUE: Уникальность: год + сем + уровень + профиль
        constraints = [
            models.UniqueConstraint(
                fields=['year_of_learning_start', 'num_of_semesters_of_study',
                        'type_of_higher_education', 'profile'],
                name='curriculum_year_num_type_profile_unique'
            )
        ]
        verbose_name = 'Учебный план'  # Название в админке
        verbose_name_plural = 'Учебные планы'  # название во мн.числе

    # Вывод таблицы в админке
    def __str__(self):
        return (f'{self.profile} | '
                f'{self.type_of_higher_education} | '
                f'{self.year_of_learning_start} | '
                f'{self.num_of_semesters_of_study} сем'
                )

# СПРАВОЧНИК ДИСЦИПЛИН
class Subject(models.Model):
    """Единый список дисциплин (Базы данных, Алгоритмизация и т.д.)."""
    id_subject = models.AutoField(primary_key=True)  # SERIAL PRIMARY KEY

    SUBJECT_CHOICES = [
        ('Автоматизация решения ОиРЗ в КИС', 'Автоматизация решения ОиРЗ в КИС'),
        ('Базы данных', 'Базы данных'),
        ('Алгоритмизация, программирование', 'Алгоритмизация, программирование'),
        ('Высокоуровневые методы программирования', 'Высокоуровневые методы программирования'),
    ]
    # название дисциплины из SUBJECT_CHOICES
    name_of_subject = models.CharField(
        max_length=100,
        choices=SUBJECT_CHOICES,
        unique=True   # нужно, чтобы не повторялись
    )

    class Meta:
        db_table = 'subjects'  # название таблицы в БД
        verbose_name = 'Дисциплина'  # человеческое название, выводится в админке
        verbose_name_plural = 'Дисциплины'  # множественное число названия таблицы

    def __str__(self):  # строковая функция - для вывода в админке
        return self.name_of_subject

# Дисциплина-Семестр (learning_subjects)
class LearningSubject(models.Model):
    """В каком семестре какую дисциплину изучают
    по конкретному учебному плану."""
    id_learning_subjects = models.AutoField(primary_key=True)

    # связи ForeignKey
    # внешний ключ с таблицей Дисциплина
    subject = models.ForeignKey(
        Subject,
        on_delete=models.RESTRICT,
        db_column='id_subject'
    )
    # внешний ключ с таблицей Учебный план
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.RESTRICT,
        db_column='id_curriculum'
    )
    # семестр после изучения >=1
    semester_after_learning = models.SmallIntegerField(
        validators=[MinValueValidator(1)]  # семестр ≥ 1
    )

    class Meta:
        db_table = 'learning_subjects'  # название таблицы в БД
        constraints = [models.UniqueConstraint(fields=['subject',
                                               'curriculum', 'semester_after_learning'],
                                               name='curric_semes_subject_unique'
            )
        ]
        verbose_name = 'Изученный предмет'  # Человеческое название в БД
        verbose_name_plural = 'Изученные предметы'  # во мн.числе

    def __str__(self):  # вывод в админке в виде строки
        return f'{self.subject} - семестр изучения {self.semester_after_learning} | {self.curriculum} '

    def subject_with_semester(self):
        """
        Удобное представление для выпадающих списков:
        Возвращает строку вида:
        «Базы данных (отзыв доступен с семестра 3)»
        """
        return f'{self.subject.name_of_subject} (отзыв доступен с семестра {self.semester_after_learning})'


# Отзывы
class Review(models.Model):
    """Текстовый отзыв студента/менеджера на дисциплину с оценкой тональности."""
    SCORE_CHOICES = [
        ('Негативный',   'Негативный'),
        ('Нейтральный',  'Нейтральный'),
        ('Положительный','Положительный'),
    ]
    # id отзыва - уникальный ключ
    id_review = models.AutoField(primary_key=True)
    # дата загрузки отзыва
    date_of_loading = models.DateField(auto_now_add=True)          # дата не NULL
    # Кто оставил отзыв (студент )
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        limit_choices_to={'role__in': ['студент', 'менеджер']},
        db_column='id'
    )
    # По какой дисциплине отзыв - внешний ключ с таблицей Дисциплина
    learning_subject = models.ForeignKey(
        LearningSubject,
        on_delete=models.RESTRICT,
        db_column='id_learning_subjects'
    )
    # текст отзыва - макс. длина 512 симв, должен быть уникальным
    review = models.CharField(
        max_length=512,
        unique=True,
        validators=[MaxLengthValidator(512)]   # CHECK char_length(review) <= 512
    )
    # балл отзыва - 0.0-негативный, 1.0-нейтральный, 2.0-положительный
    # может быть пустым, может быть не заполнен, однако при щагрузке менеджером и студентом заполняется нейронкой
    score_of_review = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0)]  # диапазон
    )
    # название оценки из вариантов SCORE_CHOICES
    # может быть пустым, может быть не заполнен, однако при щагрузке менеджером и студентом заполняется нейронкой
    name_of_score = models.CharField(
        max_length=15,
        choices=SCORE_CHOICES,
        null=True,
        blank=True
    )
    # кто физически нажал «Загрузить». Если пусто - студент, если нет - точно менеджер
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reviews_uploaded',
        db_column='uploaded_by_id',
        verbose_name='Загрузил'
    )

    class Meta:
        db_table = 'reviews'  # название таблицы в БД
        verbose_name = 'Отзыв'  # человеческое название таблицы
        verbose_name_plural = 'Отзывы'  # мн. число названия таблицы
        # ограничения уникальности
        # Один пользователь – один отзыв на дисциплину
        constraints = [models.UniqueConstraint(fields=['learning_subject',
                                               'user'], name='user_subj__unique'
            )
        ]

    def __str__(self):  # строковый вывод
        return f'Отзыв #{self.id_review} на дисциплину "{self.learning_subject}" от ({self.user})'

# ГРУППЫ СТУДЕНТОВ
class StudentGroup(models.Model):
    """Учебная группа, привязанная к учебному плану."""
    id_student_group = models.AutoField(primary_key=True)
    # учебный план - внешний ключ с таблицей Учебный план
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.RESTRICT,
        db_column='id_curriculum'
    )

    class Meta:
        db_table = 'student_group'  # название таблицы в БД
        # уникальность 2 полей
        unique_together = ('id_student_group', 'curriculum')
        verbose_name = 'Студенческая группа'  # человеческое название таблицы
        verbose_name_plural = 'Студенческие группы'  # мн. число

    def __str__(self):  # строковый вывод
        return f'Группа {self.id_student_group} (уч. план {self.curriculum})'

# СТУДЕНТ (связь 1-к-1 с User и группой)
class Student(models.Model):
    """Студент = пользователь + конкретная учебная группа."""
    # можно создать студента только имеющего статус студент в таблице accounts_user
    id_student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.RESTRICT,
        limit_choices_to={'role': 'студент'},
        db_column='id_student'
    )
    # внешний ключ с таблицей Студенческие группы
    student_group = models.OneToOneField(
        StudentGroup,
        on_delete=models.RESTRICT,
        db_column='id_student_group'
    )

    class Meta:
        db_table = 'students'  # название таблицы в БД
        # уникальность 2 полей
        unique_together = ('id_student', 'student_group')
        verbose_name = 'Студент'  # человеческое название таблицы
        verbose_name_plural = 'Студенты'  # мн.число названия таблицы

    def __str__(self):  # строковый вывод таблицы в админке Django
        return f'{self.id_student} – группа {self.student_group}'
