from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User

from .models import EventAttendees, Event, Announcement
from employee.models import Employee

# Create your views here.


@login_required(login_url='login')
def events(request):
    role    = str(request.user.groups.all()[0])
    path    = role + "/"

    events = Event.objects.all()
    
    attendedEvents = None
    if role == 'guest':
        attendedEvents = EventAttendees.objects.filter(
            guest=request.user.guest)

    if request.method == "POST":
        if "filter" in request.POST:
            if (request.POST.get("type") != ""):
                events = events.filter(
                    eventType__contains=request.POST.get("type"))

            if (request.POST.get("name") != ""):
                events = events.filter(
                    location__contains=request.POST.get("location"))

            if (request.POST.get("fd") != ""):
                events = events.filter(
                    startDate__gte=request.POST.get("fd"))

            if (request.POST.get("ed") != ""):
                events = events.filter(
                    endDate__lte=request.POST.get("ed"))

            context = {
                "role":         role,
                "events":       events,
                "type":         request.POST.get("type"),
                "location":     request.POST.get("location"),
                "fd":           request.POST.get("fd"),
                "ed":           request.POST.get("ed")
            }
            return render(request, path + "events.html", context)

        if 'Save' in request.POST:
            n       = request.POST.get('id-text')
            temp    = EventAttendees.objects.get(id=request.POST.get('id-2'))
            temp.numberOfDependees = n
            temp.save()

        if 'attend' in request.POST:  # attend button clicked
            attendedEvents = EventAttendees.objects.filter(guest=request.user.guest)
            tempEvent = events.get(id=request.POST.get('id'))
            check = False
            for t in attendedEvents:
                if t.event.id == tempEvent.id:
                    check = True
                    break
            if not check:  # event not in the query set
                eveent_obj = EventAttendees(event=tempEvent, guest=request.user.guest)
                eveent_obj.save()
                return redirect('events')  # refresh page

        elif 'remove' in request.POST:  # remove button clicked
            tempEvent = events.get(id=request.POST.get('id'))
            EventAttendees.objects.filter(event=tempEvent, guest=request.user.guest).delete()
            return redirect('events')  # refresh page

    context = {
        "role":             role,
        'events':           events,
        'attendedEvents':   attendedEvents,
        "type":             request.POST.get("type"),
        "location":         request.POST.get("location"),
        "fd":               request.POST.get("fd"),
        "ed":               request.POST.get("ed")
    }
    return render(request, path + "events.html", context)

@ login_required(login_url='login')
def announcements(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    announcements = Announcement.objects.all()
    context = {
        "role": role,
        'announcements': announcements
    }

    if request.method == "POST":
        if 'sendAnnouncement' in request.POST:  # send button clicked
            sender = request.user.employee

            announcement = Announcement(
                sender=sender, content=request.POST.get('textid'))

            announcement.save()
            return redirect('announcements')

        if "filter" in request.POST:
            if (request.POST.get("id") != ""):
                announcements = announcements.filter(
                    id__contains=request.POST.get("id"))

            if (request.POST.get("content") != ""):
                announcements = announcements.filter(
                    content__contains=request.POST.get("content"))

            if (request.POST.get("name") != ""):
                users = User.objects.filter(
                    Q(first_name__contains=request.POST.get("name")) | Q(last_name__contains=request.POST.get("name")))
                employees = Employee.objects.filter(user__in=users)
                announcements = announcements.filter(sender__in=employees)

            if (request.POST.get("date") != ""):
                announcements = announcements.filter(
                    date=request.POST.get("date"))

        context = {
            "role": role,
            'announcements': announcements,
            "id": request.POST.get("id"),
            "name": request.POST.get("name"),
            "content": request.POST.get("content"),
            "date": request.POST.get("date")
        }
        return render(request, path + "announcements.html", context)

    return render(request, path + "announcements.html", context)

@login_required(login_url='login')
def deleteAnnouncement(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    announcement = Announcement.objects.get(id=pk)
    if request.method == "POST":
        announcement.delete()
        return redirect('announcements')

    context = {
        "role": role,
        'announcement': announcement

    }
    return render(request, path + "deleteAnnouncement.html", context)