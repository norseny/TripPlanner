from django.forms import Form, ModelForm, inlineformset_factory, formset_factory

from tripplanner.models import *


class TripForm(ModelForm):
    class Meta:
        model = Trip
        exclude = ()


class AttractionForm(ModelForm):
    class Meta:
        model = Attraction
        exclude = ()


# AttractionFormSet = inlineformset_factory(Trip, Attraction, form=AttractionForm, extra=1)

AttractionFormSet = formset_factory(Attraction, extra=1)

