from django.contrib import admin
from .models import Contact, Student, Response, Message, Result

admin.site.register(Contact)
admin.site.register(Student)
admin.site.register(Message)
admin.site.register(Result)
admin.site.register(Response)
