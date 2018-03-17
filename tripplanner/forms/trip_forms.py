from django.forms import Form, ModelForm, inlineformset_factory, formset_factory, Textarea

from tripplanner.models import *
from django import forms

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'


class TripForm(ModelForm, Form):
    class Meta:
        model = Trip
        fields = ['name', 'description']
        exclude = ()
        widgets = {
          'description': Textarea(attrs={'rows':3, 'cols':'70'}),
        }


class AttractionForm(ModelForm):
    class Meta:
        model = Attraction
        exclude = ()
        widgets= {
            'start_time': DateTimeInput(), #todo: ???
            'end_time': DateTimeInput(),
        }


class JourneyForm(ModelForm):
    class Meta:
        model = Journey
        exclude = (),
        widgets= {
            'start_time': DateTimeInput(),
            'end_time': DateTimeInput(),
        }


class AccomodationForm(ModelForm):
    class Meta:
        model = Accomodation
        exclude = ()
        widgets= {
            'start_time': DateTimeInput(),
            'end_time': DateTimeInput(),
        }


AttractionFormSet = inlineformset_factory(Trip, Attraction, form=AttractionForm, extra=1, max_num=10, min_num=0)
JourneyFormSet = inlineformset_factory(Trip, Journey, form=JourneyForm, extra=1)
AccomodationFormSet = inlineformset_factory(Trip, Accomodation, form=AccomodationForm, extra=1)

# AttractionFormSet = formset_factory(Attraction, extra=1)
