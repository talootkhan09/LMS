import email
from pickle import TRUE
from unicodedata import category, name
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from .manager import UserManager

class User(AbstractUser):
    username=None
    nick_name =models.CharField(max_length=150)
    email = models.EmailField(unique= TRUE)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= []

class Student(models.Model):
    user =models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    name= models.CharField(max_length=200, null=True)
    phone= models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("student",kwargs={'pk':self.pk})     

class Book(models.Model):      
    name = models.CharField(max_length=200, null=True)
    price= models.FloatField(null=True)
    category=models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("book_detail",kwargs={'pk':self.pk})    

class Order(models.Model):
    STATUS= (
        ('Borrow','Borrow'),
    )
    student =models.ForeignKey(Student, null=True, on_delete=models.SET_NULL, related_name='order')
    book =models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    status =models.CharField(max_length=200, null=True, choices=STATUS)
    date_created =models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.status)
    def get_absolute_url(self):
        return reverse("home")