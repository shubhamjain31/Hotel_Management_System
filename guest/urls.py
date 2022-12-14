from django.urls import path
from . import views

urlpatterns = [
    path('guests/', views.guests, name="guests"),
    path('guest-edit/<str:pk>', views.guest_edit, name="guest-edit"),
    path('guest-profile/<str:pk>', views.guest_profile, name="guest-profile"),
]