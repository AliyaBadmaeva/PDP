from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/main.html'
    login_url = '/accounts/login/'  # куда отправлять неавторизованных


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


def about_page(request):
    role_docs = {
        'студент':     'docs/student_manual.pdf',
        'преподаватель': 'docs/teacher_manual.pdf',
        'менеджер':    'docs/manager_manual.pdf',
    }
    return render(request, 'blog/about.html', {
        'manual_url': role_docs.get(request.user.role, ''),
    })





