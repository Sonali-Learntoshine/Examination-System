from Teacher import views as teacher_views
from django.urls import path
from . import views

app_name = 'exam'
urlpatterns = [
    path('ajax-get-subject-list/', views.get_subject_list, name='ajax-subject-list'),
    path('', views.IndexView.as_view(), name='index-page'),

    path('add-new-exam/', views.AddExam.as_view(), name='add-new-exam'),
    path('exam/<slug:slug>/', views.ExamDetail.as_view(), name='exam-details'),
    path('exam/<int:qp_id>/<int:user_id>/appear/', views.exam_view, name='exam-appear'),

    path('add-subject/', views.AddSubject.as_view(), name='add-subject'),

    path('<slug:slug>/create-question-paper/', views.AddQuestionPaper.as_view(), name='add-question-paper'),
    path('<slug:slug>/question-paper/<int:pk>/', views.ViewQuestionPaper.as_view(), name='view-question-paper'),
    path('<slug:slug>/question-paper/<int:pk>/responses/', teacher_views.ResponseList.as_view(),
         name='view-response-list'),
    path('<slug:slug>/question-paper/<int:paper_id>/responses/<str:username>/<int:pk>/',
         teacher_views.ResponseDetail.as_view(),
         name='view-response-detail'),
    path('del-question-paper/<int:pk>/', views.DeleteQuestionPaper.as_view(), name='del-question-paper'),

    path('add-question/<int:pk>/<str:type>/', views.add_question_popup, name='add-question'),
    path('edit-question/<slug:exam>/<int:pk>/', views.EditQuestion.as_view(), name='edit-question'),
    # path('edit-question/<slug:exam>/<int:pk>/', views.update_question_popup, name='EditQuestionView'),
    path('delete-question/<int:pk>/', views.DeleteQuestion.as_view(), name='delete-question'),

    path('<int:exam_id>/<str:username>/<int:paper_id>/', views.question_paper_check_finish, name='save-result'),

    path('success/', views.generic.TemplateView.as_view(template_name='module/success.html')),
    path('temp/', views.generic.TemplateView.as_view(template_name='module/temp.html')),
    path('ajax-save-marks/', views.ajaxSubmission, name='ajax-save-marks'),
    path('ajax/', views.saveResponse, name='ajaxSubmission'),
    path('ajax-get-subject-list/', views.get_subject_list, name='ajax-subject-list'),
    path('login/', views.log_in, name='login'),

]
