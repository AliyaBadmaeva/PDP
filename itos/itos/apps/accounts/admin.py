from django.contrib import admin
from .models import Review, User, LearningSubject, Subject, Curriculum, Student
from .models import StudentGroup, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

admin.site.register(User)
admin.site.register(LearningSubject)
admin.site.register(Subject)
admin.site.register(Curriculum)
admin.site.register(Student)
admin.site.register(StudentGroup)
admin.site.register(Profile)




@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id_review', 'user', 'learning_subject',
                    'date_of_loading', 'uploaded_by')
