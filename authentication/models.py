from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# Create your models here.

class Guest(models.Model):
    user            = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phoneNumber     = PhoneNumberField(unique=True)

    def __str__(self):
        return str(self.user)

    # def numOfBooking(self):
    #     return Booking.objects.filter(guest=self).count()

    # def numOfDays(self):
    #     totalDay = 0
    #     bookings = Booking.objects.filter(guest=self)
    #     for b in bookings:
    #         day = b.endDate - b.startDate
    #         totalDay += int(day.days)

    #     return totalDay

    # def numOfLastBookingDays(self):
    #     try:
    #         return int((Booking.objects.filter(guest=self).last().endDate - Booking.objects.filter(guest=self).last().startDate).days)
    #     except:
    #         return 0

    # def currentRoom(self):
    #     booking = Booking.objects.filter(guest=self).last()
    #     return booking.roomNumber