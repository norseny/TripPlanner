from django.forms import Form, ModelForm, inlineformset_factory, Textarea, TextInput, Select, NumberInput, DateTimeInput

from tripplanner.models import *
from django import forms


dict_of_textinput_attrs = {'class': 'form-control form-control-sm'}
dict_of_datetime_range_attrs = {'class': 'datetimepicker-range form-control form-control-sm'}


class MyDateTimeInput(forms.DateTimeInput):
     input_type = 'datetime'


class MyDateTimeField(forms.DateTimeField):
    widget = MyDateTimeInput(
         attrs={'class': 'form-control form-control-sm'},
         format='%d/%m/%Y (%H:%M)'
    )


class TripForm(ModelForm, Form):
    class Meta:
        model = Trip
        fields = ['name', 'description']
        exclude = ()
        widgets = {
            'description': Textarea(attrs={'rows': 2, 'cols': '65', 'class':'materialize-textarea form-control form-control-sm'}),
            'name': TextInput(attrs=dict_of_textinput_attrs)
        }


class JourneyForm(ModelForm):
    start_time = MyDateTimeField(required=False)
    end_time = MyDateTimeField(required=False)

    class Meta:
        model = Journey
        fields = ['means_of_transport','name','start_point', 'end_point', 'start_time', 'end_time','price']
        widgets = {
            'means_of_transport': Select(attrs={'class': 'custom-select form-control-sm'}),
            'start_point': TextInput(attrs=dict_of_textinput_attrs),
            'end_point': TextInput(attrs=dict_of_textinput_attrs),
            'price': NumberInput(attrs=dict_of_textinput_attrs),
        }
        exclude = ('name',)


class AccommodationForm(ModelForm):
    start_time = MyDateTimeField(required=False)
    end_time = MyDateTimeField(required=False)


    class Meta:
        model = Accommodation
        fields = ['name','address','start_time', 'end_time', 'price']
        widgets = {
            'name': TextInput(attrs=dict_of_textinput_attrs),
            'address': TextInput(attrs=dict_of_textinput_attrs),
            'price': NumberInput(attrs=dict_of_textinput_attrs),
        }
        exclude = ()


class AttractionForm(ModelForm):
    start_time = MyDateTimeField(required=False)

    class Meta:
        model = Attraction
        fields = ['name','address','start_time', 'price']
        widgets = {
            'name': TextInput(attrs=dict_of_textinput_attrs),
            'address': TextInput(attrs=dict_of_textinput_attrs),
            'price': NumberInput(attrs=dict_of_textinput_attrs),
        }
        exclude = ()


AttractionFormSet = inlineformset_factory(Trip, Attraction, form=AttractionForm, extra=1)
JourneyFormSet = inlineformset_factory(Trip, Journey, form=JourneyForm, extra=1)

AccommodationFormSet = inlineformset_factory(Trip, Accommodation, form=AccommodationForm, extra=1)


class AddParticipantForm(Form):
    username = forms.CharField(max_length=50)


class ImageUploadForm(ModelForm):
    """Image upload form """
    class Meta:
        model = Trip
        fields = ['main_image']

