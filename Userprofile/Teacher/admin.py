from django.contrib import admin
from .models import ExamModel, Questions, Faculty


class FacultyAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'dept', 'is_active']


admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Questions)
admin.site.register(ExamModel)
