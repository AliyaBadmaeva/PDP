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

class FaqView(TemplateView):
    template_name = 'blog/faq.html'
    login_url = '/login/'  # куда отправлять неавторизованных

class ContactView(TemplateView):
    template_name = 'blog/contact.html'
    login_url = '/login/'          # куда отправлять неавторизованных
class AboutView(TemplateView):
    template_name = 'blog/about.html'
    login_url = '/login/'  # куда отправлять неавторизованных

class NlpView(TemplateView):
    template_name = 'blog/nlp.html'
    login_url = '/login/'  # куда отправлять неавторизованных


class EdaView(TemplateView):
    template_name = 'blog/eda.html'
    login_url = '/login/'  # куда отправлять неавторизованных



class BlogView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.role == 'Преподаватель':
            context['dashboard_link_text'] = 'Статистика'
            context['dashboard_link_url'] = '/dashboard/statistics/'
        elif user.role == 'Менеджер':
            context['dashboard_link_text'] = 'Загрузить отзывы'
            context['dashboard_link_url'] = '/dashboard/upload_reviews/'
        elif user.role == 'Студент':
            context['dashboard_link_text'] = 'Написать отзыв'
            context['dashboard_link_url'] = '/dashboard/write_review/'

        return context