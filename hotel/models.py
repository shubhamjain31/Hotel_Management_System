from django.db import models

# Create your models here.

class Event(models.Model):
    EVENT_TYPES = (
        ('Movie', 'Movie'),
        ('Theater', 'Theater'),
        ('Conference', 'Conference'),
        ('Concert', 'Concert'),
        ('Entertainment', 'Entertainment'),
        ('Live Music', 'Live Music'),
    )

    eventType           = models.CharField(max_length=20, choices=EVENT_TYPES)
    location            = models.CharField(max_length=100)
    startDate           = models.DateField()
    endDate             = models.DateField()
    explanation         = models.TextField()

    def __str__(self):
        return str(self.eventType)


class EventAttendees(models.Model):
    event               = models.ForeignKey(Event, on_delete=models.CASCADE)
    numberOfDependees   = models.IntegerField(default=0)
    guest               = models.ForeignKey("guest.Guest",   null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.event) + " " + str(self.guest)