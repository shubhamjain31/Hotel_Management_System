from django import forms
from django.forms import ModelForm

from .models import *

class CreateEmployeeForm(ModelForm):
    phoneNumber = forms.CharField(error_messages={
        'required'            : 'Please Enter Mobile'
    },widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mobile',
    }))
    salary = forms.CharField(error_messages={
        'required'            : 'Please Enter Salary'
    },widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Salary',
    }))
    class Meta:
        model = Employee
        fields = ['phoneNumber', 'salary']

class EditEmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ["phoneNumber", "salary"]