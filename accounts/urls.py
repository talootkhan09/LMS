from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.register_page, name="register"),
	path('login/', views.login_page, name="login"),
	path('logout/', views.logout_user, name="logout"),

    path('', views.home, name="home"),
    path('user/', views.user_page, name="user-page"),
    path('books/', views.books, name='books'),
    path('student/<str:pk_test>/', views.student, name="student"),

    path('create_order/<str:pk>/', views.create_order, name="create_order"),
    path('update_order/<str:pk>/', views.update_order, name="update_order"),
    path('delete_order/<str:pk>/', views.delete_order, name="delete_order"),
    path('bill_order/<str:pk>/',views.bill_order, name="bill"),

    path('create_student/', views.create_student, name="create_student"),
    path('delete_student/<str:pk>/', views.delete_student, name="delete_student"),

    path('create_book/', views.create_book, name="create_book"),
    path('delete_book/<str:pk>/', views.delete_book, name="delete_book"),


]
