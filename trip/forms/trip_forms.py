from django.forms import ModelForm, inlineformset_factory

from trip.models import *


class TripForm(ModelForm):
    class Meta:
        model = Trip
        exclude = ()


class AttractionForm(ModelForm):
    class Meta:
        model = Attraction
        exclude = ()


AttractionFormSet = inlineformset_factory(Trip, Attraction,
                                            form=AttractionForm, extra=1)
