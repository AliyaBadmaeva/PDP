def dashboard_button(request):
    if not request.user.is_authenticated:
        return {}
    role = request.user.role
    mapping = {
        'менеджер':   {'text': 'Загрузить отзывы',   'url': 'dashboard:manager'},
        'преподаватель': {'text': 'Статистика',      'url': 'dashboard:teacher'},
        'студент':    {'text': 'Написать отзыв',    'url': 'dashboard:student'},
    }
    return {'dashboard_button': mapping.get(role)}