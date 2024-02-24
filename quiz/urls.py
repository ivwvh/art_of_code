from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='quiz-home'),
    path('about/', views.about, name='quiz-about')
]