from django import forms

class LoginForm(forms.Form):  # Форма авторизации
    username = forms.CharField(label='Логин', max_length=100)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
