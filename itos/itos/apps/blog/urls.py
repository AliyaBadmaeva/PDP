from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    path('',          views.MainView.as_view(),   name='main'),
    path('faq/',      views.FaqView.as_view(),   name='faq'),
    path('about/',    views.about_page, name='about'),
    path('contacts/',  views.ContactView.as_view(), name='contacts'),
    path('nlp/', views.NlpView.as_view(), name='nlp'),
    path('eda/', views.EdaView.as_view(), name='eda'),
]
