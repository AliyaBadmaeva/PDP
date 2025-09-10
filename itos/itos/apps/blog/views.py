from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/main.html'
    login_url = '/accounts/login/'  # куда отправлять неавторизованных

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.role == 'преподаватель':
            context['dashboard_link_text'] = 'Статистика'
            context['dashboard_link_url'] = '/dashboard/teacher_dashboard/'
        elif user.role == 'менеджер':
            context['dashboard_link_text'] = 'Загрузить отзывы'
            context['dashboard_link_url'] = '/dashboard/manager_dashboard/'
        elif user.role == 'студент':
            context['dashboard_link_text'] = 'Написать отзыв'
            context['dashboard_link_url'] = '/dashboard/student_dashboard/'
        return context

class FaqView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/faq.html'
    login_url = '/accounts/login/'

class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/contacts.html'
    login_url = '/accounts/login/'
class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/about.html'
    login_url = '/accounts/login/'  # куда отправлять неавторизованных

class NlpView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/nlp.html'
    login_url = '/accounts/login/'  # куда отправлять неавторизованных


class EdaView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/eda.html'
    login_url = '/accounts/login/'  # куда отправлять неавторизованных






