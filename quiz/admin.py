from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(QuizAssignment)
admin.site.register(QuizResult)
admin.site.register(Statistics)
