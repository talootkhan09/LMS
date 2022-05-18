from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)
from .models import *
from . import models
from .forms import CreateUserForm,StudentForm
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
        email = request.POST.get('email')
        password =request.POST.get('password')

        user = authenticate(request, email=email, password=password)

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
    orders= request.user.student.order.all()
    context = {'orders':orders, 'id':id}
    return render(request, 'accounts/user.html', context)

class BookListView(LoginRequiredMixin, ListView):
    model = models.Book

class BookDetailView(LoginRequiredMixin,DetailView):
    context_object_name = 'book_details'
    model = models.Book
    template_name = 'accounts/book_detail.html'

class BookCreateView(PermissionRequiredMixin,CreateView):
    permission_required = 'book.add_books'
    fields = ("name","price","category")
    model = models.Book

class BookUpdateView(PermissionRequiredMixin,UpdateView):
    permission_required = 'book.change_books'
    fields = ("name","price")
    model = models.Book

class BookDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required = 'book.delete_books'
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

class StudentDetailView(PermissionRequiredMixin,DetailView):
    permission_required = 'student.view_students'
    context_object_name = 'student_details'
    model = models.Student
    template_name = 'accounts/student_detail.html'    

class StudentUpdateView(PermissionRequiredMixin,UpdateView):
    permission_required = 'student.change_students'
    fields = ('email',)
    model = models.Student

class StudentDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required = 'student.delete_students'
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
