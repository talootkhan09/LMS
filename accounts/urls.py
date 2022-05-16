from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.register_page, name="register"),
	path('login/', views.login_page, name="login"),
	path('logout/', views.logout_user, name="logout"),

    path('', views.home, name="home"),
    path('user/', views.user_page, name="user-page"),
    path('books/', views.BookListView.as_view(), name='books'),
    path('student/<str:pk_test>/', views.student, name="student"),

    path('create_order/<str:pk>/', views.OrderCreateView.as_view(), name="create_order"),
    path('update_order/<str:pk>/', views.OrderUpdateView.as_view(), name="update_order"),
    path('delete_order/<str:pk>/', views.OrderDeleteView.as_view(), name="delete_order"),
    path('bill_order/<str:pk>/',views.bill_order, name="bill"),

    path('create_student/', views.create_student, name="create_student"),
    path('delete_student/<str:pk>/', views.StudentDeleteView.as_view(), name="delete_student"),
    path('update_student/<str:pk>/', views.StudentUpdateView.as_view(), name="update_student"),

    path('create_book/', views.BookCreateView.as_view(), name="create_book"),
    path('book_detail/<str:pk>/', views.BookDetailView.as_view(), name="book_detail"),
    path('delete_book/<str:pk>/', views.BookDeleteView.as_view(), name="delete_book"),
    path('update_book/<str:pk>/', views.BookUpdateView.as_view(), name="update_book"),


]
