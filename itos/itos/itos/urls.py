from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

admin.site.site_header = "Администратор ИТОС"
admin.site.site_title = "Портал администратора ИТОС"
admin.site.index_title = "Добро пожаловать в ИТОС!"

urlpatterns = [
    path('admin/', admin.site.urls),  # админка Django
    path('', RedirectView.as_view(url='/blog/', permanent=False)),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
]


