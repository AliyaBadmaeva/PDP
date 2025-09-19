# Главный конфиг Django-проекта itos.
# Загружает переменные окружения (.env), подключается к PostgreSQL через JDBC,
# очищает сессии при остановке сервера в dev-режиме.
import os
from pathlib import Path
from dotenv import load_dotenv
import jaydebeapi     # JDBC-драйвер для СУБД
import signal, sys, atexit   # обработка Ctrl+C и штатного выхода

# ОКРУЖЕНИЕ
load_dotenv()  # берём SECRET_KEY, DEBUG, DB_* и пр. из .env

# Корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Добавляем папку apps в PYTHONPATH, чтобы писать для импорта from accounts.models import ...
sys.path.insert(0, str(BASE_DIR / 'apps'))

# Секретные данные
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Домены/IP, с которых разрешён доступ к Django
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# пути после авторизации
AUTH_USER_MODEL = 'accounts.User'  # кастомная модель пользователя
LOGIN_URL = '/accounts/login/'   # куда идти, если не авторизован
LOGIN_REDIRECT_URL = '/'   # после успешного входа


# Приложения
INSTALLED_APPS = [
    "django.contrib.admin",  # чтобы использовать встроенную админку Джанго
    "django.contrib.auth",
    'django_extensions',
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
    "accounts",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "itos.urls"

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.dashboard_button',  # Кнопка в ЛК
            ],
        },
    },
]

WSGI_APPLICATION = "itos.wsgi.application"

# БАЗА ДАННЫХ
# Подключаемся к PostgreSQL через JDBC-драйвер (jaydebeapi)
conn = jaydebeapi.connect(
    "org.postgresql.Driver",
    "jdbc:postgresql://localhost:5432/itos",
    ["postgres", "do_j12498!"],
    "postgresql-42.7.7.jar"  # относительный путь к jar - jar лежит рядом с manage.py
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# СТАТИКА / МЕДИА

STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ЛОКАЛИЗАЦИЯ
LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ОЧИСТКА СЕССИЙ ПРИ ВЫХОДЕ (dev-режим)
# все сессии удаляются в режиме разработчика
def logout_all(signum=None, frame=None):
    """Удаляет все сессии и корректно завершает процесс."""
    from django.contrib.sessions.models import Session
    Session.objects.all().delete()
    print('\n Все сессии удалены (dev-режим)')
    sys.exit(0)


# регистрируем на Ctrl+C и штатное завершение
signal.signal(signal.SIGINT, logout_all)
atexit.register(logout_all)













