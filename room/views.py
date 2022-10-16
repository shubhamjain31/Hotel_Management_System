from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages

from .models import Booking, Room
from guest.models import Guest
from validators import is_invalid

import datetime

# Create your views here.

@login_required(login_url='login')
def bookings(request):
    role    = str(request.user.groups.all()[0])
    path    = role + "/"

    bookings = Booking.objects.all()
    # calculating total for every booking:
    totals = {}  # <booking : total>
    for booking in bookings:
        start_date      = datetime.datetime.strptime(str(booking.startDate), "%Y-%m-%d")
        end_date        = datetime.datetime.strptime(str(booking.endDate), "%Y-%m-%d")
        numberOfDays    = abs((end_date-start_date).days)

        # get room peice:
        price   = Room.objects.get(number=booking.roomNumber.number).price
        total   = price * numberOfDays
        totals[booking] = total

    if request.method == "POST":
        if "filter" in request.POST:
            if (request.POST.get("number") != ""):
                rooms = Room.objects.filter(
                    number__contains=request.POST.get("number"))
                bookings = bookings.filter(
                    roomNumber__in=rooms)

            if (request.POST.get("name") is not None):
                users    = User.objects.filter(Q(first_name__contains=request.POST.get("name")) | Q(last_name__contains=request.POST.get("name")))
                guests   = Guest.objects.filter(user__in=users)
                bookings = bookings.filter(guest__in=guests)

            if (request.POST.get("rez") != ""):
                bookings = bookings.filter(dateOfReservation=request.POST.get("rez"))

            if (request.POST.get("fd") != ""):
                bookings = bookings.filter(startDate__gte=request.POST.get("fd"))

            if (request.POST.get("ed") != ""):
                bookings = bookings.filter(endDate__lte=request.POST.get("ed"))

            context = {
                "role": role,
                'bookings': bookings,
                'totals': totals,
                "name": request.POST.get("name") or '',
                "number": request.POST.get("number"),
                "rez": request.POST.get("rez"),
                "fd": request.POST.get("fd"),
                "ed": request.POST.get("ed")
            }

            return render(request, path + "bookings.html", context)

    context = {
        "role": role,
        'bookings': bookings,
        'totals': totals
    }
    return render(request, path + "bookings.html", context)

@login_required(login_url='login')
def room_profile(request, id):
    role        = str(request.user.groups.all()[0])
    path        = role + "/"
    tempRoom    = Room.objects.get(number=id)
    bookings    = Booking.objects.filter(roomNumber=tempRoom)
    guests      = Guest.objects.all()
    bookings2   = Booking.objects.all()

    context = {
        "role": role,
        "bookings": bookings,
        "room": tempRoom,
        "guests": guests,
        "bookings2": bookings2
    }

    if request.method == "POST":
        if "lockRoom" in request.POST:
            fd      = request.POST.get("bsd")
            ed      = request.POST.get("bed")
            fd      = datetime.datetime.strptime(fd, '%Y-%m-%d')
            ed      = datetime.datetime.strptime(ed, '%Y-%m-%d')
            check   = True
            for b in bookings:
                if b.endDate >= fd.date() and b.startDate <= ed.date():
                    check = False
                    break
            if check:
                tempRoom.statusStartDate    = fd
                tempRoom.statusEndDate      = ed
                tempRoom.save()
            else:
                messages.error(request, "There is a booking in the interval!")
        if "unlockRoom" in request.POST:
            tempRoom.statusStartDate    = None
            tempRoom.statusEndDate      = None
            tempRoom.save()

        if "deleteRoom" in request.POST:
            check = True
            for b in bookings:
                if b.startDate <= datetime.datetime.now().date() or b.endDate >= datetime.datetime.now().date():
                    check = False
            if check:
                tempRoom.delete()
                return redirect("rooms")
            else:
                messages.error(request, "There is a booking in the interval!")

    return render(request, path + "room-profile.html", context)

@login_required(login_url='login')
def deleteBooking(request, pk):
    role    = str(request.user.groups.all()[0])
    path    = role + "/"

    booking = Booking.objects.get(id=pk)
    if request.method == "POST":
        booking.delete()
        return redirect('bookings')

    context = {
        "role": role,
        'booking': booking

    }
    return render(request, path + "deleteBooking.html", context)