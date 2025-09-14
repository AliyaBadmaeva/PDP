
from django.urls import path
from . import views

app_name = "reviews"
urlpatterns = [
    path("upload/", views.upload_reviews, name="upload"),
    path("add/", views.student_review, name="student_add"),
    path("export/", views.export_reviews, name="export"),
]