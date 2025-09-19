# WSGI-конфигурация для проекта itos.
# Используется продакшн-сервером (gunicorn, uWSGI, mod_wsgi) для запуска Django-приложения.
import os
from django.core.wsgi import get_wsgi_application

# Указываем Django, где находится модуль настроек (переменная окружения обычно задаётся в systemd/docker)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itos.settings")

# Создаём WSGI-приложение, которое будет обрабатывать HTTP-запросы
application = get_wsgi_application()
