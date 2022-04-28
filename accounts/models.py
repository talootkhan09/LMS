from telnetlib import STATUS
from unicodedata import category, name
from django.db import models

class Student(models.Model):
    name= models.CharField(max_length=200, null=True)
    phone= models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
     GENRE = (
         ('Physics', 'Physics'),
         ('Computer','Computer'),
     )       
     name = models.CharField(max_length=200, null=True)
     price= models.FloatField(null=True)
     category=models.CharField(max_length=200, null=True, choices=GENRE)

     def __str__(self):
        return self.name

class Order(models.Model):
    STATUS= (
        ('Borrow','Borrow'),
        ('Return', 'Return'),
    ) 
    student =models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    book =models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    status =models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.status
    