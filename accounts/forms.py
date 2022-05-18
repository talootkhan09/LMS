from dataclasses import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms



from .models import Order, Student, Book, User


class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['email', 'password1', 'password2']

class StudentForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['email', 'password1', 'password2']	

class BookForm(ModelForm):
	class Meta:
		model = Book
		fields = '__all__'		
