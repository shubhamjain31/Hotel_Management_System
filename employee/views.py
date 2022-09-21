from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db.models import Q

from .models import Employee, Task

# Create your views here.

@login_required(login_url='login')
def employee_details(request, pk):
    if request.method == 'POST':
        user        = User.objects.get(id=pk)
        employee    = Employee.objects.get(user=user)
        
        user.first_name         = request.POST.get("first_name")
        user.last_name          = request.POST.get("last_name")
        # user.email              = request.POST.get("email")
        employee.phoneNumber    = request.POST.get("phoneNumber")
        user.save()
        employee.save()
        messages.success(request, "Profile Updated!")
        return redirect("home")

    role = str(request.user.groups.all()[0])
    path = role + "/"

    tempUser    = User.objects.get(id=pk)
    employee    = Employee.objects.get(user=tempUser)
    tasks       = Task.objects.filter(employee=employee)
    context = {
        "role": role,
        "employee": employee,
        "tasks": tasks
    }
    return render(request, path + "employee-profile.html", context)

@login_required(login_url='login')
def employees(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    employees = Employee.objects.all()

    if request.method == "POST":
        if "filter" in request.POST:
            users = User.objects.all()
            if (request.POST.get("id") != ""):
                users = users.filter(
                    id__contains=request.POST.get("id"))
                employees = employees.filter(user__in=users)

            if (request.POST.get("name") != ""):
                users = users.filter(
                    Q(first_name__contains=request.POST.get("name")) | Q(last_name__contains=request.POST.get("name")))
                employees = employees.filter(user__in=users)

            if (request.POST.get("email") != ""):
                users = users.filter(email__contains=request.POST.get("email"))
                employees = employees.filter(user__in=users)

            if (request.POST.get("number") != ""):
                employees = employees.filter(
                    phoneNumber__contains=request.POST.get("number"))

            if (request.POST.get("filterRole") != ""):
                try:
                    group = Group.objects.get(
                        name__contains=request.POST.get("filterRole"))
                except:
                    group = None
                users = users.filter(groups=group)
                employees = employees.filter(user__in=users)

        context = {
            "role": role,
            "employees": employees,
            "id": request.POST.get("id"),
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "number": request.POST.get("number"),
            "filterRole": request.POST.get("filterRole")
        }
        return render(request, path + "employees.html", context)

    context = {
        "role": role,
        "employees": employees
    }
    return render(request, path + "employees.html", context)