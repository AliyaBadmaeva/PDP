# Корневой URL-конфигуратор проекта itos.
# Подключает админку, приложения и задаёт заголовки админ-интерфейса.

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# Заголовки в админке
admin.site.site_header = "Администратор ИТОС"  # верхняя строка
admin.site.site_title = "Портал администратора ИТОС"  # <title>
admin.site.index_title = "Добро пожаловать в ИТОС!"  # заголовок на главной

urlpatterns = [
    # заголовок на главной
    path('admin/', admin.site.urls),  # админка Django
    # Корень сайта - сразу переводим на блог
    path('', RedirectView.as_view(url='/blog/', permanent=False)),
    # Подключаем URL-ы приложений
    path('blog/', include('blog.urls')),  # информационные страницы
    path('accounts/', include('accounts.urls')),  # вход / выход / редирект по ролям
    path('dashboard/', include('dashboard.urls')),  # личные кабинеты (student, teacher, manager)
]


