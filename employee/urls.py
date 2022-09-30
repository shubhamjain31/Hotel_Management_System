from django.urls import path
from . import views

urlpatterns = [
    path('employee-add/', views.add_employee, name="add-employee"),
    path('employee-profile/<str:pk>/', views.employee_details, name="employee-profile"),
    path('employee-edit/<str:pk>/', views.employee_details_edit, name="employee-edit"),
    path('employees/', views.employees, name="employees"),

    path('tasks/', views.tasks, name="tasks"),
]