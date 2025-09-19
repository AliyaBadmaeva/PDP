# URL-маршруты приложения blog (информационные страницы сайта)
from django.urls import path
from . import views

# Пространство имён позволяет обращаться к url-ам через
# {% url 'blog:main' %}, {% url 'blog:faq' %} и т.д.
app_name = 'blog'


urlpatterns = [
    path('',          views.MainView.as_view(),   name='main'),  # Главная страница
    path('faq/',      views.FaqView.as_view(),   name='faq'),  # FAQ
    path('about/',    views.about_page, name='about'),  # «О программе» – реализована через функцию-представление
    path('contacts/',  views.ContactView.as_view(), name='contacts'),  # Контакты
    path('nlp/', views.NlpView.as_view(), name='nlp'),  # Страница «Технологии NLP»
    path('eda/', views.EdaView.as_view(), name='eda'),  # Страница «Разведочный анализ данных (EDA)»
]
