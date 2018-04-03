from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import django
from datetime import datetime
from decimal import *



class MeansOfTransport(models.Model):
    name = models.CharField(max_length=50, unique=True)
    name_pl = models.CharField(max_length=50)

    def __str__(self):
        lang = django.utils.translation.get_language()
        if lang == 'pl':
            return self.name_pl
        return self.name


class BasicInfo(models.Model):
    start_time = models.DateTimeField(null=True, blank=True, default=datetime.now)
    end_time = models.DateTimeField(null=True, blank=True, default=datetime.now)
    price = models.DecimalField(decimal_places=2, max_digits=8, null=True, blank=True, default=0.00)

    class Meta:
        abstract = True


class Trip(BasicInfo):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, max_length=250, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # todo:szablony wycieczek- inna klasa

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('trip-detail', kwargs={'pk': self.pk})

    def update_dates_and_price(self, journeys, accommodations, attractions):
        start_times = set()
        end_times = set()
        all_details = journeys + accommodations + attractions

        for el in all_details:

            if ('start_time' in el) and ('start_time' is not None):
                start_times.add(el['start_time'])
            if ('end_time' in el) and ('end_time'is not None):
                end_times.add(el['end_time'])
            if 'price' in el:
                self.price += el['price']

        self.start_time = min(start_times)
        self.end_time = max(end_times)
        self.save()


class Journey(BasicInfo):
    start_point = models.CharField(max_length=250, null=True, blank=True)
    # todo: quicksearch cities/countries - googlemaps dest?
    end_point = models.CharField(max_length=250, null=True, blank=True)
    # todo: moze dodac bool srodek publiczny/prywatny jak publiczny, to reusable dla innych użytkowników
    means_of_transport = models.ForeignKey(MeansOfTransport, on_delete=models.SET_NULL, null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Accommodation(BasicInfo):
    place = models.CharField(max_length=250, null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Attraction(BasicInfo):
    place = models.CharField(max_length=250, null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
