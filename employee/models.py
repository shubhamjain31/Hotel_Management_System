from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

import uuid

# Create your models here.

class Employee(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user            = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phoneNumber     = PhoneNumberField(unique=True)
    salary          = models.FloatField()

    def __str__(self):
        return str(self.user)

class Task(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    employee        = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    startTime       = models.DateTimeField()
    endTime         = models.DateTimeField()
    description     = models.TextField()

    def str(self):
        return str(self.employee)