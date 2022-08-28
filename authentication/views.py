from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group, User

from .forms import CreateUserForm
from .models import Guest

# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username or Password is incorrect")

        context = {}
        return render(request, 'authentication/login.html', context)

def register_page(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                if (len(User.objects.filter(email=request.POST.get("email"))) != 0):
                    messages.error(
                        request, 'Email address is already taken')
                    return redirect('login')

                user        = form.save()
                username    = form.cleaned_data.get('username')

                group       = Group.objects.get(name="guest")
                user.groups.add(group)

                curGuest = Guest(
                    user=user, phoneNumber=request.POST.get("phoneNumber"))
                curGuest.save()

                messages.success(
                    request, 'Guest Account Was Created Succesfully For ' + username)

                return redirect('login')

        context = {'form': form}
        return render(request, 'authentication/register.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')