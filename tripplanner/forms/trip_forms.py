from django.forms import Form, ModelForm, inlineformset_factory, Textarea, TextInput, Select, NumberInput, DateTimeInput

from tripplanner.models import *
from tripcore import settings
from django import forms

from bootstrap_daterangepicker import widgets, fields
from tripplanner import additional

dict_of_textinput_attrs = {'class': 'form-control form-control-sm'}
dict_of_datetime_range_attrs = {'class': 'datetimepicker-range form-control form-control-sm'}


class MyDateTimeInput(forms.DateTimeInput):
     input_type = 'datetime'


class MyDateTimeField(forms.DateTimeField):
    # input_formats = settings.DATETIME_INPUT_FORMATS,
    widget = MyDateTimeInput(
         attrs={'class': 'form-control form-control-sm'},
         format='%d/%m/%Y (%H:%M)'
    )

#
# class MyDateTimeRangeField(fields.DateTimeRangeField):
#         clearable=True,
#         input_formats=settings.DATETIME_INPUT_FORMATS
#         widget=widgets.DateTimeRangeWidget(
#             attrs= dict_of_datetime_range_attrs,
#             format='%d/%m/%Y (%H:%M)'
#         )


class MyTextDateTimeRangeField(forms.CharField):
    widget = forms.TextInput(
         attrs=dict_of_datetime_range_attrs
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
    datetime_range = MyTextDateTimeRangeField()

    class Meta:
        model = Journey
        fields = ['start_point', 'end_point',
                  'datetime_range',
                  'means_of_transport','name','price'
                    # ,'start_time', 'end_time'
                  ]
        widgets = {
            'means_of_transport': Select(attrs={'class': 'custom-select form-control-sm'}),
            'name': TextInput(attrs=dict_of_textinput_attrs),
            'start_point': TextInput(attrs=dict_of_textinput_attrs),
            'end_point': TextInput(attrs=dict_of_textinput_attrs),
            'price': TextInput(attrs=dict_of_textinput_attrs),
            # 'end_time': TextInput(attrs={'class':'d-none'}),
            # 'start_time': TextInput(attrs={'class':'d-none'}),
            'end_time': TextInput(),
            'start_time': TextInput(),
        }
        exclude = ()

    def clean(self):
        if self.is_valid():
            # change daterange to none if default values
            if self.cleaned_data['datetime_range']:
                self.cleaned_data['datetime_range'] = additional.check_daterange(self.cleaned_data['datetime_range'])
                # assign start and end time from datetime range
                if self.cleaned_data['datetime_range']:
                    self.cleaned_data['start_time'] = self.cleaned_data['datetime_range'][0]
                    self.cleaned_data['end_time'] = self.cleaned_data['datetime_range'][1]


class AccommodationForm(ModelForm):
    datetime_range = MyTextDateTimeRangeField()

    class Meta:
        model = Accommodation
        fields = ['name', 'address','datetime_range', 'price']
        widgets = {
            'name': TextInput(attrs=dict_of_textinput_attrs),
            'address': TextInput(attrs=dict_of_textinput_attrs),
            'price': NumberInput(attrs=dict_of_textinput_attrs),
            'end_time': TextInput(attrs={'class':'d-none'}),
            'start_time': TextInput(attrs={'class':'d-none'}),
        }
        exclude = ()

    def clean(self):
        if self.is_valid():
            # change daterange to none if default values
            if self.cleaned_data['datetime_range']:
                self.cleaned_data['datetime_range'] = additional.check_daterange(self.cleaned_data['datetime_range'])
                # assign start and end time from datetime range
                if self.cleaned_data['datetime_range']:
                    self.cleaned_data['start_time'] = self.cleaned_data['datetime_range'][0] #todo: nie zapisuje start date i end date
                    self.cleaned_data['end_time'] = self.cleaned_data['datetime_range'][1]


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

