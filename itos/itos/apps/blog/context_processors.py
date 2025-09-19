# Контекст-процессор, добавляющий во *все* шаблоны переменную dashboard_button
# с текстом и URL кнопки «Личный кабинет» в зависимости от роли пользователя.

def dashboard_button(request):
    """
    Возвращает словарь вида:
    {'dashboard_button': {
              'text': 'Написать отзыв',
              'url': 'dashboard:student'
          }
        }
    либо пустой словарь, если пользователь не аутентифицирован.
    Использование в шаблонах html:
            {% if dashboard_button %}
              <a href="{% url dashboard_button.url %}">
                {{ dashboard_button.text }}
              </a>
            {% endif %}
    """
    # Анонимным пользователям (не студент, не менеджер, не преподаватель) кнопка не показывается
    if not request.user.is_authenticated:
        return {}
    role = request.user.role  # получение роли
    # Сопоставление роли → текст + имя URL-маршрута
    mapping = {
        'менеджер':   {'text': 'Загрузить отзывы',   'url': 'dashboard:manager'},
        'преподаватель': {'text': 'Статистика',      'url': 'dashboard:teacher'},
        'студент':    {'text': 'Написать отзыв',    'url': 'dashboard:student'},
    }
    # Возвращаем словарь, который Django добавит в context каждого шаблона
    return {'dashboard_button': mapping.get(role)}
