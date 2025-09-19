# Контроллеры для информационных (общедоступных) страниц сайта.
# Доступ разрешён только авторизованным пользователям (LoginRequiredMixin).
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

# CBV (class-based-views)-страницы (TemplateView)
# Все классы проверяют авторизацию и при необходимости редиректят на /accounts/login/
class MainView(LoginRequiredMixin, TemplateView):  # Главная страница блога
    template_name = 'blog/main.html'  # имя шаблона
    login_url = '/accounts/login/'  # куда отправлять неавторизованных


class FaqView(LoginRequiredMixin, TemplateView):  # FAQ – ответы на частые вопросы.
    template_name = 'blog/faq.html'  # имя шаблона
    login_url = '/accounts/login/'  # куда отправлять неавторизованных

class ContactView(LoginRequiredMixin, TemplateView):  # Контакты.
    template_name = 'blog/contacts.html'  # имя шаблона
    login_url = '/accounts/login/'  # куда отправлять неавторизованных
class AboutView(LoginRequiredMixin, TemplateView):
    """Описание программы (CBV-заглушка, фактически используется about_page)."""
    template_name = 'blog/about.html'  # имя шаблона
    login_url = '/accounts/login/'  # куда отправлять неавторизованных

class NlpView(LoginRequiredMixin, TemplateView):
    """Страница «Технологии NLP»."""
    template_name = 'blog/nlp.html'  # имя шаблона
    login_url = '/accounts/login/'  # куда отправлять неавторизованных


class EdaView(LoginRequiredMixin, TemplateView):
    # Страница «Разведочный анализ данных (EDA)».
    template_name = 'blog/eda.html'  # имя шаблона
    login_url = '/accounts/login/'  # куда отправлять неавторизованных

# Функциональное представление
def about_page(request):
    """
    Описание программы + ссылка на руководство пользователя.
    Раздаёт разные PDF-файлы в зависимости от роли.
    """
    # Соответствие роль - путь к PDF-инструкции
    role_docs = {
        'студент':     'docs/student_manual.pdf',
        'преподаватель': 'docs/teacher_manual.pdf',
        'менеджер':    'docs/manager_manual.pdf',
    }
    # request.user уже авторизован (LoginRequiredMixin в URLconf)
    return render(request, 'blog/about.html', {
        'manual_url': role_docs.get(request.user.role, ''),  # пусто, если роль не найдена
    })





