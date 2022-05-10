from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm,StudentForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from .constants import ADMIN, STUDENT

@unauthenticated_user
def registerPage(request):

<<<<<<< HEAD
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
=======
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			useremail= form.cleaned_data.get('email')

			group = Group.objects.get(name='student')
			user.groups.add(group)
			Student.objects.create(
>>>>>>> 2e2e15d917552dfcb8a5d3967789936df997672f
				user=user,
				name=user.username,
				email=user.email,
				)

<<<<<<< HEAD
            messages.success(request, f"Account was created for {username}" )
=======
			messages.success(request, 'Account was created for ' + username +'with email' + useremail)
>>>>>>> 2e2e15d917552dfcb8a5d3967789936df997672f

            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

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

def logoutUser(request):
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
def userPage(request):
    orders= request.user.student.order_set.all()
    context = {'orders':orders}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN,STUDENT])
def books(request):
    books = Book.objects.all()

    return render(request, 'accounts/books.html', {'books':books})

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
def createOrder(request,pk):
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
@allowed_users(allowed_roles=[ADMIN])
def updateOrder(request, pk):

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
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN])
def createStudent(request):
<<<<<<< HEAD
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
=======
	form = StudentForm()
	if request.method == 'POST':
		form = StudentForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			useremail= form.cleaned_data.get('email')

			group = Group.objects.get(name='student')
			user.groups.add(group)
			Student.objects.create(
>>>>>>> 2e2e15d917552dfcb8a5d3967789936df997672f
				user=user,
				name=user.username,
				email=user.email,
				)

<<<<<<< HEAD
            messages.success(request, f"Account was created for {username}" )
=======
			messages.success(request, 'Account was created for ' + username +'with email' + useremail)
>>>>>>> 2e2e15d917552dfcb8a5d3967789936df997672f

            return redirect('/')

<<<<<<< HEAD

    context = {'form':form}
    return render(request, 'accounts/student_form.html', context)
=======
	context = {'form':form}
	return render(request, 'accounts/student_form.html', context)
>>>>>>> 2e2e15d917552dfcb8a5d3967789936df997672f

@login_required(login_url='login')
@allowed_users(allowed_roles=[ADMIN])
def deleteStudent(request, pk):
<<<<<<< HEAD
    student = Student.objects.get(id=pk)
    if request.method == "POST":
        student.delete()
        return redirect('/')

    context = {'student':student}
    return render(request, 'accounts/deleteStudent.html', context)
=======
	student = Student.objects.get(id=pk)
	if request.method == "POST":
		student.delete()
		return redirect('/')

	context = {'student':student}
	return render(request, 'accounts/deleteStudent.html', context)
	
>>>>>>> 2e2e15d917552dfcb8a5d3967789936df997672f
