'''from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Получение данных из БД
def index(request):
    return render(request, 'index.html')

@login_required
def blog(request):
    return render(request, 'main.html')'''

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/main.html'
    login_url = '/login/'          # куда отправлять неавторизованных