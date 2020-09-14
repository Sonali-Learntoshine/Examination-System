from django.urls import path
from . import views
import Exam_module.views as exam_views

app_name = 'teacher'
urlpatterns = [
    # path('exam/', views.add_exam, name='add_exam'),
    path('exam/', views.AddExam.as_view(), name='add_exam'),
    path('exam/<slug:slug>/', exam_views.ExamDetail.as_view(), name='exam-details'),
    path('add_question/', views.add_question, name='add_question'),
    path('add_student/', views.add_student, name='add_student'),
    path('view_question/', views.view_question, name='view_question'),
    path('view_exam/', views.view_exam, name='view_exam'),
    path('view_exam/<int:id>/', views.view_exam_question, name='view_exam_question'),
    path('update_question/<int:id>/', views.update_question, name='update_question'),
    path('hod_add_exam/', exam_views.AddExam.as_view(), name='hod_add_exam'),
    path('view_question/<int:pk>/delete', views.DeleteQuestion.as_view(), name='delete_question'),
    path('signup', views.Registration.as_view(), name='signup'),
    path('login', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/delete/', views.DeleteFacultyProfile.as_view(), name='delete-profile'),
    path('activate/<int:pk>/', views.activate, name='profile-activate'),
    path('dashboard/<int:pk>/', views.FacultyDashboard.as_view(), name='dashboard'),
    path('ajax-query', views.ajax_query, name='ajax-query')
]
'''
< td >
< button

class ="btn btn-sm btn-danger mb-1" style="width: 60px"


onclick = "DeleteConfirmation('{% url 'teacher:delete-profile' teacher.user_id %}?next={{ request.path|urlencode }}')" >
delete
< / button >
< button


class ="btn btn-sm btn-warning mb-1" style="width: 60px"


onclick = "window.location.href='{% url 'teacher:profile' teacher.user_id %}'" >
view
< / button >
< / td >
'''
