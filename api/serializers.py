from rest_framework import serializers
 
from accounts.models import Student, User, Book
 
class StudentSerializer(serializers.ModelSerializer):
 
    class Meta:
 
        model = Student
 
        exclude= ['user']

class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
 
        model = User
 
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
 
    class Meta:
 
        model = Book
 
        fields = '__all__'
