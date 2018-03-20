from django.forms import Form, ModelForm, inlineformset_factory, formset_factory, Textarea

from tripplanner.models import *
from django import forms
from tripcore import settings


class MyDateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'

# class MyDateTimeField(forms.DateTimeField):
#     input_formats = settings.DATETIME_INPUT_FORMATS
#     widget = MyDateTimeInput(
#         attrs={'placeholder': 'date'}
#     )


class TripForm(ModelForm, Form):
    class Meta:
        model = Trip
        fields = ['name', 'description']
        exclude = ()
        widgets = {
            'description': Textarea(attrs={'rows': 3, 'cols': '70'}),
        }


class JourneyForm(ModelForm):
    start_time = forms.DateTimeField( # todo: jakos tego nie powtarzac
        input_formats=settings.DATETIME_INPUT_FORMATS, #todo: validation : start date cannot be later than enddate
        widget=MyDateTimeInput
    )
    end_time = forms.DateTimeField(
        input_formats=settings.DATETIME_INPUT_FORMATS,
        widget=MyDateTimeInput
    )

    class Meta:
        model = Journey
        exclude = (),


class AccommodationForm(ModelForm):
    start_time = forms.DateTimeField(
        input_formats=settings.DATETIME_INPUT_FORMATS,
        widget=MyDateTimeInput
    )
    end_time = forms.DateTimeField(
        input_formats=settings.DATETIME_INPUT_FORMATS,
        widget=MyDateTimeInput
    )
    class Meta:
        model = Accommodation
        exclude = ()


class AttractionForm(ModelForm):
    start_time = forms.DateTimeField(
        input_formats=settings.DATETIME_INPUT_FORMATS,
        widget=MyDateTimeInput()
    )
    end_time = forms.DateTimeField(
        input_formats=settings.DATETIME_INPUT_FORMATS,
        widget=MyDateTimeInput()
    )
    class Meta:
        model = Attraction
        exclude = ()


AttractionFormSet = inlineformset_factory(Trip, Attraction, form=AttractionForm, extra=1)
JourneyFormSet = inlineformset_factory(Trip, Journey, form=JourneyForm, extra=1)
AccommodationFormSet = inlineformset_factory(Trip, Accommodation, form=AccommodationForm, extra=1)
