from django.urls import path
from . import views

urlpatterns = [
    path('employee-add/', views.add_employee, name="add-employee"),
    path('employee-profile/<str:pk>/', views.employee_details, name="employee-profile"),
    path('employees/', views.employees, name="employees"),
]