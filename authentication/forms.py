from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CreateUserForm(UserCreationForm):
    username = forms.CharField(error_messages={
        'required'            : 'Please Enter Username'
    },widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    first_name = forms.CharField(error_messages={
        'required'            : 'Please Enter First Name'
    },widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name',
    }))
    last_name = forms.CharField(error_messages={
        'required'            : 'Please Enter Last Name'
    },widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name',
    }))
    email = forms.EmailField(error_messages={
        'required'            : 'Please Enter Email'
    },widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
    }))
    password1 = forms.CharField(error_messages={
        'required'            : 'Please Enter Password'
    },widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder': 'Password',
    }))
    password2 = forms.CharField(error_messages={
        'required'            : 'Please Enter Confirm-Password'
    },widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder': 'Re-Password',
    }))


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class editGuest(ModelForm):
    class Meta:
        model = Guest
        fields = ["phoneNumber"]

class ROLES(forms.Form):
    ROLES_TYPES = [
        ('manager', 'manager'),
        ('receptionist', 'receptionist'),
        ('staff', 'staff'),
    ]
    ROLES_TYPES = forms.CharField(
        widget=forms.RadioSelect(choices=ROLES_TYPES))