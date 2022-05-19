from dataclasses import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Order, Student, Book, User
from django.contrib.auth import get_user_model

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("email","nick_name", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email address"
	
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
		
