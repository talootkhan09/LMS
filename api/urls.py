from django.urls import path
from django.contrib import admin
 
from . import views
 
urlpatterns = [
 
path('student-api/', views.student_list),
path('user-api/', views.user_list),
path('book-api/', views.book_list),
 
]