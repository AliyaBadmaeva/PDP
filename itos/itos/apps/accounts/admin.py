# интерфейс админики для всех модулей приложения accounts
from django.contrib import admin
# импорт моделей БД, которые будут отображаться в админке
from .models import Review, User, LearningSubject, Subject, Curriculum, Student
from .models import StudentGroup, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

# Регистрация моделей в базовом режиме, без кастомизации
admin.site.register(User)  # Пользователи (кастомная модель)
admin.site.register(LearningSubject)  # Учебные дисциплины
admin.site.register(Subject)         # Справочник дисциплин
admin.site.register(Curriculum)      # Учебные планы
admin.site.register(Student)         # Студенты
admin.site.register(StudentGroup)    # Учебные группы
admin.site.register(Profile)         # Профили подготовки


# Кастомизированная админка для модели отзывов
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Интерфейс просмотра/изменения отзывов.
    Удобно для быстрого поиска, фильтрации и проверки загруженных данных.
    """
    list_display = ('id_review',  # Первичный ключ отзыва
                    'user',           # Кто оставил отзыв
                    'learning_subject',  # По какой ИТ-дисциплине
                    'date_of_loading',   # Дата загрузки (для аудита)
                    'uploaded_by'        # Кто фактически загрузил (важно при массовом импорте)
                    )
