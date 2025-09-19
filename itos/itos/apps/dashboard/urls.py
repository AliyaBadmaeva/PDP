# URL-маршруты приложения dashboard (личные кабинеты по ролям, импорт/экспорт отчётов)
from django.urls import path
from . import views
# Импортируем функцию-контроллер для выгрузки Excel-файла
from .views import export_reviews_to_excel

# Пространство имён: позволяет обращаться {% url 'dashboard:manager' %} и т.д.
app_name = 'dashboard'

urlpatterns = [
    # Центральный редирект (определяет роль и перебрасывает на нужный дашборд)
    path('', views.DashboardRedirectView.as_view(), name='index'),
    # Личный кабинет менеджера (загрузка отзывов из Excel - достпуно только менеджеру)
    path('manager/',   views.ManagerDashboardView.as_view(), name='manager'),
    # Личный кабинет студента (написание отзывов - доступно только студенту)
    path('student/',   views.StudentDashboardView.as_view(), name='student'),
    # Личный кабинет преподавателя (просмотр инструкции)
    path('teacher/',   views.TeacherDashboardView.as_view(), name='teacher'),
    # Экспорт последних 900 000 отзывов в Excel (доступен преподавателю)
    path('export/reviews/', export_reviews_to_excel, name='export_reviews'),
]
