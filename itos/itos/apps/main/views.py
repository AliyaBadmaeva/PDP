from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Получение данных из БД
def index(request):
    return render(request, 'index.html')

@login_required
def main(request):
    return render(request, 'main.html')