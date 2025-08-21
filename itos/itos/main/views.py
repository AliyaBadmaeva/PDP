from django.shortcuts import render

# Получение данных из БД
def index(request):
    return render(request, 'index.html')