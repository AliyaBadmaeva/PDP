from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog:main')  # Переход на главную страницу блога
        else:
            return render(request, 'accounts/login.html', {'error': 'Неправильное имя пользователя или пароль'})
    else:
        return render(request, 'accounts/login.html')


@login_required
def role_redirect(request):
    if request.user.is_authenticated:
        user_name = request.user.name
        user_patronymic = request.user.patronymic
        user_role = request.user.role
        if user_role == 'менеджер':
            return redirect('dashboard:manager')
        elif user_role == 'преподаватель':
            return redirect('dashboard:teacher')
        elif user_role == 'студент':
            return redirect('dashboard:student')
        else:
            return render(request, 'index.html', {'error': 'Неизвестная роль пользователя'})
    else:
        return render(request, 'index.html', {'error': 'Пользователь не идентифицирован'})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # Переход на страницу входа после выхода

