from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('books/', views.books, name='books'),
    path('student/<str:pk_test>/', views.student, name="student"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('create_student/', views.createStudent, name="create_student"),
    path('delete_student/<str:pk>/', views.deleteStudent, name="delete_student"),

    path('create_book/', views.createBook, name="create_book"),
    path('delete_book/<str:pk>/', views.deleteBook, name="delete_book"),


]
