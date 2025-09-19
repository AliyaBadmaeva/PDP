# Маршруты URL-шаблоны приложения accounts
# Префикс app_name = 'accounts' позволяет обращаться к url-ам через {% url 'accounts:login' %}
from django.urls import path
from . import views

app_name = 'accounts'  # namespace для всего приложения

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Страница авторизации
    path('logout/', views.logout_view, name='logout'),  # Выход из системы
    # Корень приложения («/accounts/») – редирект на нужный дашборд
    # в зависимости от роли пользователя
    path('', views.role_redirect, name='role_redirect'),
]
