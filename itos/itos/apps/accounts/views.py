# Контроллеры авторизации / выхода и перенаправления по ролям
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
import logging
logger = logging.getLogger(__name__)


def login_view(request):
    """
    Вход в систему.
    GET – показываем форму.
    POST – проверяем учётные данные и переводим на главную блога или возвращаем ошибку.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # создаём сессию
            next_url = request.GET.get('next', reverse('blog:main'))
            logger.info(f"Перенаправление на {next_url}")  # логирование
            return redirect(next_url)  # Перенаправление на главную страницу блога или на URL из параметра next
        else:
            # Неверная пара логин/пароль
            logger.warning("Неправльная аутентификация")
            return render(request, 'accounts/login.html', {'error': 'Неправильное имя пользователя или пароль'})
    else:
        # Показ пустой формы
        return render(request, 'accounts/login.html')


@login_required
def role_redirect(request):
    """
    Центральный «распределитель» после логина.
    Переводит пользователя на свой дашборд в зависимости от роли.
    """
    if request.user.is_authenticated:
        user_role = request.user.role
        if user_role == 'менеджер':
            return redirect('dashboard:manager')
        elif user_role == 'преподаватель':
            return redirect('dashboard:teacher')
        elif user_role == 'студент':
            return redirect('dashboard:student')
        else:
            # Роль не опознана – возвращаем на главную с ошибкой
            return render(request, 'index.html', {'error': 'Неизвестная роль пользователя'})
    else:
        return render(request, 'index.html', {'error': 'Пользователь не идентифицирован'})


def logout_view(request):
    # Выход из системы и перенаправление на страницу входа.
    logout(request)  # убиваем сессию
    return redirect('accounts:login')  # Переход на страницу входа после выхода

