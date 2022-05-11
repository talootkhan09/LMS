from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm,StudentForm, BookForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from .constants import ADMIN, STUDENT

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

@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN,STUDENT])
def books(request):
    books = Book.objects.all()

    return render(request, 'accounts/books.html', {'books':books})

@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN])
def create_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()

            Book.objects.create(
				name=book.name,
				price=book.price,
				category=book.category
				)

            return redirect('books')

    context = {'form':form}
    return render(request, 'accounts/book_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN])
def delete_book(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == "POST":
        book.delete()
        return redirect('/books')

    context = {'book':book}
    return render(request, 'accounts/deleteBook.html', context)

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

@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN,STUDENT])
def create_order(request,pk):
    OrderFormSet = inlineformset_factory(Student, Order, fields=('book', 'status'), extra=5 )
    student = Student.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=student)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=student)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form':formset}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN,STUDENT])
def update_order(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

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

@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN])
def delete_student(request, pk):
    student = Student.objects.get(id=pk)
    if request.method == "POST":
        student.delete()
        return redirect('/')

    context = {'student':student}
    return render(request, 'accounts/deleteStudent.html', context)
