from urllib import request
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView,TemplateView, View)
from .models import *
from . import forms
from . import models
from .forms import CreateUserForm,StudentForm, UserCreateForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from .constants import ADMIN, STUDENT
from datetime import date

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/register.html"
    def post(self, request, *args, **kwargs):
        pass
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.save()

            group = Group.objects.get(name='student')

            user.groups.add(group)
            Student.objects.create(
				user=user,
				name=user.nick_name,
				email=user.email,
				)

            return redirect('login')

class LoginView(View):

    def post(self, request):
        email = request.POST['email']
        password =request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/dashboard.html', context)            

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

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class Home(PermissionRequiredMixin,TemplateView):
    permission_required = 'book.add_books'
    template_name = "accounts/dashboard.html"
    context_object_name = 'student'
    model = models.Student
    def handle_no_permission(self):
        messages.info(self.request ,self.permission_denied_message)
        # or specific redirects based on context 
        return redirect('books')

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['student'] = Student.objects.all()
        context['orders'] = Order.objects.all()
        return context

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

