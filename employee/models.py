from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Employee(models.Model):
    user            = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phoneNumber     = PhoneNumberField(unique=True)
    salary          = models.FloatField()

    def __str__(self):
        return str(self.user)

class Task(models.Model):
    employee        = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    startTime       = models.DateTimeField()
    endTime         = models.DateTimeField()
    description     = models.TextField()

    def str(self):
        return str(self.employee)