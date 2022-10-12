from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.bookings, name="bookings"),
    path('room-profile/<str:id>/', views.room_profile, name="room-profile"),
]