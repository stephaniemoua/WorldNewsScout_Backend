from django.contrib import admin
from django.urls import path, include, re_path
from ProjectAPI import views

urlpatterns = [
    path('home/', views.current_datetime),
] 

