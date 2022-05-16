from datetime import datetime
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)

# Create your views here.
from .models import *
from . import models
from .forms import OrderForm, CreateUserForm,StudentForm, BookForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from .constants import ADMIN, STUDENT
from datetime import date

@unauthenticated_user
def register_page(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email= form.cleaned_data.get('email')

            group = Group.objects.get(name='student')
            user.groups.add(group)
            Student.objects.create(
				user=user,
				name=user.username,
				email=user.email,
				)

            messages.success(request, f"Account was created for {username}" )

            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    students = Student.objects.all()

    total_students = students.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'students':students,
    'total_orders':total_orders, 'total_students':total_students,
	'delivered':delivered,
    'pending':pending }

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[STUDENT])
def user_page(request):
    id= request.user.id
    orders= request.user.student.order_set.all()
    context = {'orders':orders, 'id':id}
    return render(request, 'accounts/user.html', context)

class BookListView(LoginRequiredMixin, ListView):
    model = models.Book

class BookDetailView(LoginRequiredMixin,DetailView):
    context_object_name = 'book_details'
    model = models.Book
    template_name = 'accounts/book_detail.html'

class BookCreateView(LoginRequiredMixin,CreateView):
    fields = ("name","price","category")
    model = models.Book

class BookUpdateView(LoginRequiredMixin,UpdateView):
    fields = ("name","price")
    model = models.Book

class BookDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Book
    success_url = reverse_lazy("books")

class OrderListView(LoginRequiredMixin, ListView):
    model = models.Order

class OrderCreateView(LoginRequiredMixin,CreateView):
    fields = ("student","book","status")
    model = models.Order

class OrderUpdateView(LoginRequiredMixin,UpdateView):
    fields = ("book","status")
    model = models.Order

class OrderDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Order
    success_url = reverse_lazy('home')

@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN, STUDENT])
def bill_order(request, pk):
    orders = Order.objects.get(id=pk)
    price = orders.book.price
    dates =(date.today() - orders.date_created).days
    bill =price + dates * price
    if request.method == "POST":
        orders.delete()
        return redirect('/')

    context = {'order':orders, 'price':price, 'bill':bill, 'date':dates}
    return render(request, 'accounts/bill.html',context)

class StudentDetailView(LoginRequiredMixin,DetailView):
    context_object_name = 'student_details'
    model = models.Student
    template_name = 'accounts/student_detail.html'    

@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN])
def student(request, pk_test):
    student = Student.objects.get(id=pk_test)
    orders = student.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'student':student, 'orders':orders, 'order_count':order_count,
    'myFilter':myFilter}
    return render(request, 'accounts/students.html',context)

class StudentUpdateView(LoginRequiredMixin,UpdateView):
    fields = ("phone","email")
    model = models.Student

class StudentDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Student
    success_url = reverse_lazy('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN])
def create_student(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email= form.cleaned_data.get('email')

            group = Group.objects.get(name='student')
            user.groups.add(group)
            Student.objects.create(
				user=user,
				name=user.username,
				email=user.email,
				)

            messages.success(request, f"Account was created for {username}" )

            return redirect('/')


    context = {'form':form}
    return render(request, 'accounts/student_form.html', context)
