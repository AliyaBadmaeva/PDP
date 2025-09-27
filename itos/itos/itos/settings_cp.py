# itos/settings_cp.py
"""
Настройки для БЫСТРЫХ критических тестов (Critical Path Smoke).
- отдельная тестовая БД test_itos_cp
- минимальный набор middleware
- быстрый MD5-хэшер паролей
- отключены логи
- миграции не отключаем, чтобы Django мог создать тестовую схему
"""

import logging
from .settings import *

#  База данных: отдельная, чтобы не мешать основной
DATABASES = {
    'default': {
        **DATABASES['default'],          # берём настоящую БД
        'TEST': {
            'NAME': 'test_itos_cp',       # имя тестовой БД
        },
    }
}

#  Быстрый хэшер паролей (ускоряет создание пользователей)
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

#  Минимальный middleware (меньше вызовов - быстрее тест)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#  Отключаем логи (меньше I/O - быстрее тест)
logging.disable(logging.CRITICAL)