from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count

from datetime import datetime, date, timedelta

from .models import Guest
from room.models import Booking
from hotel.models import EventAttendees
from authentication.forms import editGuest, EditUserForm, EditUserForm

# Create your views here.


@login_required(login_url='login')
def guests(request):
    role    = str(request.user.groups.all()[0])
    path    = role + "/"

    topRange = Booking.objects.all().values("guest").annotate(total=Count("guest")).order_by("-total")
    topLimit = 10
    topList = []
    for t in topRange:
        if len(topList) > 10:
            break
        else:
            topList.append(Guest.objects.get(id=t.get("guest")))

    bookings = Booking.objects.all()
    fd = datetime.combine(date.today()-timedelta(days=30), datetime.min.time())
    ld = datetime.combine(date.today(), datetime.min.time())
    guests = []

    for b in bookings:
        if b.endDate >= fd.date() and b.startDate <= ld.date():
            if b.guest not in guests:
                guests.append(b.guest)

    if request.method == "POST":
        if "filterDate" in request.POST:

            if request.POST.get("f_day") == "" and request.POST.get("l_day") == "":
                guests = Guest.objects.all()

                context = {
                    "role": role,
                    "guests": guests,
                    "fd": "",
                    "ld": ""
                }
                return render(request, path + "guests.html", context)

            if request.POST.get("f_day") == "":
                fd = datetime.strptime("1970-01-01", '%Y-%m-%d')
            else:
                fd = request.POST.get("f_day")
                fd = datetime.strptime(fd, '%Y-%m-%d')

            if request.POST.get("l_day") == "":
                ld = datetime.strptime("2030-01-01", '%Y-%m-%d')
            else:
                ld = request.POST.get("l_day")
                ld = datetime.strptime(ld, '%Y-%m-%d')

            for b in bookings:
                if b.endDate >= fd.date() and b.startDate <= ld.date():
                    if b.guest not in guests:
                        guests.append(b.guest)

        if "filterGuest" in request.POST:
            guests  = Guest.objects.all()
            users   = User.objects.all()
            
            if (request.POST.get("id") != ""):
                users = users.filter(
                    id__contains=request.POST.get("id"))
                guests = guests.filter(user__in=users)

            if (request.POST.get("name") != ""):
                users = users.filter(
                    Q(first_name__contains=request.POST.get("name")) | Q(last_name__contains=request.POST.get("name")))
                guests = guests.filter(user__in=users)

            if (request.POST.get("email") != ""):
                users = users.filter(email__contains=request.POST.get("email"))
                guests = guests.filter(user__in=users)

            if (request.POST.get("number") != ""):
                guests = guests.filter(
                    phoneNumber__contains=request.POST.get("number"))

            context = {
                "role": role,
                "guests": guests,
                "id": request.POST.get("id"),
                "name": request.POST.get("name"),
                "email": request.POST.get("email"),
                "number": request.POST.get("number")
            }
            return render(request, path + "guests.html", context)

        if "top" in request.POST:
            topRange = Booking.objects.all().values("guest").annotate(
                total=Count("guest")).order_by("-total")
            topList = []
            topLimit = request.POST.get("top")
            for t in topRange:
                if len(topList) >= int(topLimit):
                    break
                else:
                    topList.append(Guest.objects.get(id=t.get("guest")))
            context = {
                "role": role,
                "guests": guests,
                "topList": topList,
                "topLimit": topLimit,
                "fd": fd,
                "ld": ld
            }
            return render(request, path + "guests.html", context)
    context = {
        "role": role,
        "guests": guests,
        "topList": topList,
        "topLimit": topLimit,
        "fd": fd,
        "ld": ld
    }
    return render(request, path + "guests.html", context)

@login_required(login_url='login')
def guest_profile(request, pk):
    tempUser    = User.objects.get(id=pk)
    guest       = Guest.objects.get(user=tempUser)

    if request.method == 'POST':
        tempUser.first_name     = request.POST.get("first_name")
        tempUser.last_name      = request.POST.get("last_name")
        guest.phoneNumber       = request.POST.get("phoneNumber")
        tempUser.save()
        guest.save()
        return redirect("home")
    role = str(request.user.groups.all()[0])
    path = role + "/"

    eventAttendees = EventAttendees.objects.filter(guest=guest)
    bookings = Booking.objects.filter(guest=guest)
    context = {
        "role": role,
        "guest": guest,
        "eventAttendees": eventAttendees,
        "bookings": bookings
    }
    return render(request, path + "guest-profile.html", context)

@login_required(login_url='login')
def guest_edit(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"
    tempuser    = User.objects.get(id=pk)
    guest       = Guest.objects.get(user=tempuser)
    form1       = editGuest(instance=guest)
    form2       = EditUserForm(instance=tempuser)

    context = {
        "role": role,
        "guest": guest,
        "form1": form1,
        "form2": form2,
        "user": tempuser,
    }

    if request.method == "POST":
        form1       = editGuest(request.POST, instance=guest)
        form2       = EditUserForm(request.POST, instance=tempuser)
        if form1.is_valid and form2.is_valid:
            form1.save()
            form2.save()

    return render(request, path + "guest-edit.html", context)