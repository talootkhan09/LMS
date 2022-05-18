from django.contrib import admin

# Register your models here.
from .models import *

class StudentAdmin(admin.ModelAdmin):
    list_display =['name','phone','email']
    list_editable =['phone', 'email']

class BookAdmin(admin.ModelAdmin):
    search_fields=['category']

admin.site.register(Student,StudentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Order)
admin.site.register(User)