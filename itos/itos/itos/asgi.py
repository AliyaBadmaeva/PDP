# ASGI-конфигурация для проекта itos.
# Используется для запуска в production-среде (uvicorn, daphne) и при работе с WebSocket/Django Channels.

import os
from django.core.asgi import get_asgi_application

# Указываем Django, где лежит основной файл настроек
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itos.settings")
# Создаём ASGI-приложение, которое будет обрабатывать HTTP/WebSocket-запросы
application = get_asgi_application()
