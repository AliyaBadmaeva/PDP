from django.urls import path
from . import views
from .views import export_reviews_to_excel

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardRedirectView.as_view(), name='index'),
    path('manager/',   views.ManagerDashboardView.as_view(), name='manager'),
    path('student/',   views.StudentDashboardView.as_view(), name='student'),
    path('teacher/',   views.TeacherDashboardView.as_view(), name='teacher'),
    path('export/reviews/', export_reviews_to_excel, name='export_reviews'),
]
