from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class BasicInfo(models.Model):
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=8, null=True)

    class Meta:
        abstract = True


class Trip(BasicInfo):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE) # todo: wiec szablony wycieczek- inna klasa?

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('trip-detail', kwargs={'pk': self.pk})


class Journey(BasicInfo):
    start_point = models.CharField(max_length=250, null=True)
    end_point = models.CharField(max_length=250, null=True)
    means_of_transport = models.CharField(max_length=250, null=True) #todo: moze dodac bool srodek publiczny/prywatny jak publiczny, to reusable dla innych użytkowników
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Attraction(BasicInfo):
    place = models.CharField(max_length=250, null=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Accomodation(BasicInfo):
    place = models.CharField(max_length=250, null=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)