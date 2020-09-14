from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Student.urls', namespace='student')),
    path('teacher/', include('Teacher.urls', namespace='teacher')),
    path('exam_module/', include('Exam_module.urls', namespace='exam_module')),
    path('', include('Authenticate.urls')),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
