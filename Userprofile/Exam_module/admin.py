from django.contrib import admin
from .models import Subject, Question, QuestionPaper, Exam

# Register your models here.
admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(QuestionPaper)
admin.site.register(Exam)
