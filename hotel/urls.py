from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.events, name="events"),
    path('announcements/', views.announcements, name="announcements"),
    path('deleteAnnouncement/<str:pk>/',views.deleteAnnouncement, name="deleteAnnouncement"),
]