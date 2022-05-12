from unicodedata import category, name
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user =models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    name= models.CharField(max_length=200, null=True)
    phone= models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)

class Book(models.Model):      
    name = models.CharField(max_length=200, null=True)
    price= models.FloatField(null=True)
    category=models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)

class Order(models.Model):
    STATUS= (
        ('Borrow','Borrow'),
    )
    student =models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    book =models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    status =models.CharField(max_length=200, null=True, choices=STATUS)
    date_created =models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.status)
    