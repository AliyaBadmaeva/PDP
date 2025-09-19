# Конфигурация приложения blog в соответствии с версиями Django 3.2+
from django.apps import AppConfig


class MainConfig(AppConfig):
    """
    Класс-конфигуратор приложения blog.

    Атрибуты:
        default_auto_field: тип авто-инкремента для первичных ключей.
                             BigAutoField = 64-битное поле, рекомендовано
                             с Django 3.2+ (совместимость на будущее).
        name:               полный путь до приложения в формате
                             «apps.blog» или просто «blog»,
                             в зависимости от настроек INSTALLED_APPS.
    """
    # Тип первичного ключа по умолчанию для всех моделей приложения
    default_auto_field = "django.db.models.BigAutoField"
    # Путь/имя приложения в проекте
    name = "blog"
