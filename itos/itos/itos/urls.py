
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


admin.site.site_header = "Администратор ИТОС"
admin.site.site_title = "Портал администратора ИТОС"
admin.site.index_title = "Добро пожаловать в ИТОС!"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/',  auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
