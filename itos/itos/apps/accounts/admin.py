from django.contrib import admin
from .models import Review, User, LearningSubject, Subject, Curriculum, Student
from .models import StudentGroup, Profile



admin.site.register(Review)
admin.site.register(User)
admin.site.register(LearningSubject)
admin.site.register(Subject)
admin.site.register(Curriculum)
admin.site.register(Student)
admin.site.register(StudentGroup)
admin.site.register(Profile)
