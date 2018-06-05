from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import django
from decimal import *
from datetime import datetime
from django.utils.timezone import make_aware


class MeansOfTransport(models.Model):
    name = models.CharField(max_length=50, unique=True)
    name_pl = models.CharField(max_length=50)

    def __str__(self):
        lang = django.utils.translation.get_language()
        if lang == 'pl':
            return self.name_pl
        return self.name


class BasicInfo(models.Model):
    start_time = models.DateField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=50)
    more_info = models.TextField(null=True, max_length=1000, blank=True)
    class Meta:
        abstract = True


class Trip(BasicInfo):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(null=True, max_length=250, blank=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    end_time = models.DateField(null=True, blank=True)
    main_image = models.ImageField(upload_to='users_img', blank=True, null=True)
    private_trip = models.BooleanField(default=False)
    currency = models.TextField(max_length=10, default='PLN')
    participants = models.ManyToManyField(User) #todo: duration (timedelta start and endtime)

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
    end_point = models.CharField(max_length=250, null=True, blank=True)
    end_time = models.DateField(null=True, blank=True)

    means_of_transport = models.ForeignKey(MeansOfTransport, on_delete=models.SET_NULL, null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Accommodation(BasicInfo):
    name = models.CharField(null=False, blank=False, max_length=50)
    address = models.CharField(max_length=250, null=True, blank=True)
    end_time = models.DateField(null=True, blank=True)
    date_range = models.CharField(null=True, blank=True, max_length=50)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


    def save(self, force_insert=False, force_update=False):
        if self.date_range:
            self.start_end_date_from_daterange()
        else:
            self.start_time = None
            self.end_time = None
        models.Model.save(self, force_insert, force_update)

    def start_end_date_from_daterange(self):
        if 'do' in self.date_range:
            start_date, end_date = (self.date_range).split(' do ', 2)
        elif 'to' in self.date_range:
            start_date, end_date = (self.date_range).split(' to ', 2)

        self.start_time = make_aware(datetime.strptime(start_date, '%d/%m/%y'))
        self.end_time = make_aware(datetime.strptime(end_date, '%d/%m/%y'))


class Attraction(BasicInfo):
    address = models.CharField(max_length=250, null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

