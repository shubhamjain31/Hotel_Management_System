from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def home(request):
    role = str(request.user.groups.all()[0])
    
    if role != "guest":
        return redirect("employee-profile", pk=request.user.id)
    else:
        return redirect("guest-profile", pk=request.user.id)