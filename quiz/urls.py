from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.indexview, name='home'),
    
    path('about/', views.AboutView.as_view(), name='quiz-about'),
    
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('question/create/<int:quiz_id>', views.QuestionCreateView.as_view(), name='question_create'),
    path('quiz/create/', views.QuizCreateView.as_view(), name='quiz_create'),
    path('quiz/edit/<int:pk>/', views.QuizEditView.as_view(), name='quiz_edit'),

    path('test/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('submit/<int:id>', views.submit_quiz, name='submit_quiz'),
    path('delete_quiz/<int:quiz_id>/', views.delete_quiz, name='quiz_delete'),
    path('select_teacher/', views.TeacherSelectionView.as_view(), name='select_teacher'),
    path('statistics/<int:pk>/', views.QuizStatisticsView.as_view(), name='quiz_statistics'),
    path('profile/', views.profile_view, name='profile'),
]



