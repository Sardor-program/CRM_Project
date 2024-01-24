from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from .forms import RegisterForm, AddRecordForm
from .models import Records


def home(request):
    records = Records.objects.all()

    #Check to see if loggin in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged in")
            return redirect('home')
        else:
            messages.error(request, "There was a problem in Logged in. Please try again")
            return redirect('home')
    else:
        context = {
            "records": records
        }
        return render(request, 'home.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have Successfully registered")
            return redirect('home')
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form':form})


    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Records.objects.get(id=pk)
        context = {
            "customer_record": customer_record
        }
        return render(request, 'record.html', context)
    else:
        messages.success(request, "You must logged in to view that page")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        customer = Records.objects.get(id=pk)
        customer.delete()
        messages.success(request, "Record deleted successfully ")
        return redirect('home')
    else:
        messages.success(request, "You must logged in ")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record Successfully Added')
                return redirect('home')
        context = {
            "form": form
        }
        return render(request, 'add_record.html', context)
    else:
        messages.success(request, "You must br logged in")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Records.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Successfully Updated")
            return redirect('home')
        context = {
            "form": form
        }
        return render(request, 'update_record.html', context)
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')
