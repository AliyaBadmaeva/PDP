from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    path('',          views.MainView.as_view(),   name='main'),
    path('faq/',      views.FaqView.as_view(),   name='faq'),
    path('about/',    views.AboutView.as_view(),   name='about'),
    path('contact/',  views.ContactView.as_view(), name='contact'),
    path('nlp/', views.NlpView.as_view(), name='nlp'),
    path('eda/', views.EdaView.as_view(), name='eda'),
]