from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db.models import Q

from .models import Employee, Task
from .forms import CreateEmployeeForm, EditEmployeeForm
from authentication.forms import ROLES, CreateUserForm, EditUserForm

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
    # tasks       = Task.objects.filter(employee=employee)
    context = {
        "role": role,
        "employee": employee,
        # "tasks": tasks
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

def add_employee(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    form    = CreateUserForm()
    form2   = ROLES()
    form3   = CreateEmployeeForm()

    if request.method == 'POST':
        post = request.POST.copy()  # to make it mutable
        post['phoneNumber'] = "+91" + post['phoneNumber']
        request.POST = post
        print(request.POST)

        form        = CreateUserForm(request.POST)
        form2       = ROLES(request.POST)
        form3       = CreateEmployeeForm(request.POST)

        if form.is_valid() and form2.is_valid() and form3.is_valid():
            user            = form.save()
            employee        = form3.save()
            employee.user   = user
            employee.save()

            username = form.cleaned_data.get('username')

            role = form2.cleaned_data.get("ROLES_TYPES")

            group = Group.objects.get(name=role)
            user.groups.add(group)

            messages.success(
                request, role + ' Account Was Created Succesfuly For ' + username)

            return redirect('employees')
        else:
            print(form3.errors)
            print(form.errors)
    context = {
        'form': form,
        'form2': form2,
        'form3': form3,
        "role": role
    }
    return render(request, path + "add-employee.html", context)

@ login_required(login_url='login')
def employee_details_edit(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    tempuser = User.objects.get(id=pk)
    employee = Employee.objects.get(user=tempuser)

    form1 = EditEmployeeForm(instance=employee)
    form2 = EditUserForm(instance=tempuser)

    context = {
        "role": role,
        "employee": employee,
        "user": tempuser,
        "form1": form1,
        "form2": form2
    }

    if request.method == "POST":
        form1 = EditEmployeeForm(request.POST, instance=employee)
        form2 = EditUserForm(request.POST, instance=tempuser)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()

    return render(request, path + "employee-edit.html", context)

@login_required(login_url='login')
def tasks(request):
    role        = str(request.user.groups.all()[0])
    path        = role + "/"

    tempEmp     = Employee.objects.get(user=request.user)
    tasks       = Task.objects.filter(employee=tempEmp)

    context = {
        "role": role,
        'tasks': tasks
    }
    if request.method == "POST":
        if "markAsComplete" in request.POST:
            tid = request.POST.get("tid")
            Task.objects.get(id=tid).delete()
            return redirect("tasks")

        if "filter" in request.POST:
            if(request.POST.get("id") != ""):
                tasks = tasks.filter(id=request.POST.get("id"))

            if(request.POST.get("desc") != ""):
                tasks = tasks.filter(
                    description__contains=request.POST.get("desc"))

            if(request.POST.get("fd") != ""):
                tasks = tasks.filter(startTime__gte=request.POST.get("fd"))

            if(request.POST.get("ed") != ""):
                tasks = tasks.filter(endTime__lte=request.POST.get("ed"))

            context = {
                "role": role,
                "tasks": tasks,
                "id": request.POST.get("id"),
                "desc": request.POST.get("desc"),
                "fd": request.POST.get("fd"),
                "ed": request.POST.get("ed")
            }

    return render(request, path + "tasks.html", context)