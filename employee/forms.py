from django.forms import ModelForm

from .models import *

class CreateEmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['phoneNumber', 'salary']

class editEmployee(ModelForm):
    class Meta:
        model = Employee
        fields = ["phoneNumber", "salary"]