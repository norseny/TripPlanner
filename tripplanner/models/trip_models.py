from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import django
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
    start_time = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=50)
    more_info = models.TextField(null=True, max_length=1000, blank=True)
    class Meta:
        abstract = True


class Trip(BasicInfo):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(null=True, max_length=250, blank=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    end_time = models.DateTimeField(null=True, blank=True)
    main_image = models.ImageField(upload_to='static/own/img/users_img', blank=True, null=True)
    private_trip = models.BooleanField(default=False)
    participants = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('trip-detail', kwargs={'pk': self.pk})

    def update_dates_and_price(self, journeys, accommodations, attractions):
        start_times = set()
        end_times = set()
        all_details = journeys + accommodations + attractions
        total_price = Decimal(0.0)

        for el in all_details:

            if ('start_time' in el):
                if el['start_time'] is not None:
                    start_times.add(el['start_time'])
            if ('end_time' in el):
                if el['end_time'] is not None:
                    end_times.add(el['end_time'])
            if 'price' in el:
                if el['price'] is not None:
                    total_price += el['price']

        if start_times:
            self.start_time = min(start_times)
        if end_times:
            self.end_time = max(end_times)
        if isinstance(self.price, float):
            self.price = float(total_price)
        else:
            self.price = total_price
        self.save()


class Journey(BasicInfo):
    start_point = models.CharField(max_length=250, null=True, blank=True)
    # todo: quicksearch cities/countries - googlemaps dest?
    end_point = models.CharField(max_length=250, null=True, blank=True)
    # todo: moze dodac bool srodek publiczny/prywatny jak publiczny, to reusable dla innych użytkowników
    end_time = models.DateTimeField(null=True, blank=True)
    means_of_transport = models.ForeignKey(MeansOfTransport, on_delete=models.SET_NULL, null=True, blank=True)

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Accommodation(BasicInfo):
    address = models.CharField(max_length=250, null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Attraction(BasicInfo):
    address = models.CharField(max_length=250, null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
