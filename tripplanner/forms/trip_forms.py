from django.forms import Form, ModelForm, inlineformset_factory, Textarea, TextInput, Select, NumberInput, \
    CheckboxInput, EmailInput

from tripplanner.models import *
from django import forms

dict_of_textinput_attrs_autocomplete = {'class': 'form-control form-control-sm autocomplete'}
dict_of_textinput_attrs = {'class': 'form-control form-control-sm'}


class MyDateTimeInput(forms.DateTimeInput):
    input_type = 'date'

class MyDateTimeField(forms.DateTimeField):
    widget = MyDateTimeInput(
        attrs={'class': 'form-control form-control-sm datetime'},
        format='%d.%m.%Y (%H:%M)'
    )

class MyDateRangeField(forms.CharField):
    widget = TextInput(
        attrs={'class': 'form-control form-control-sm daterange'},
    )

class TripForm(ModelForm, Form):
    class Meta:
        model = Trip
        fields = ['name', 'description', 'private_trip', 'currency']
        exclude = ()
        widgets = {
            'description': Textarea(attrs={'rows': 2, 'cols': '65', 'class': 'materialize-textarea form-control '
                                                                             'form-control-sm'}),
            'name': TextInput(attrs=dict_of_textinput_attrs),
            'private_trip': CheckboxInput(attrs={'class': 'form-check',}),
            'currency': TextInput({'class': 'form-control form-control-sm', 'style' : 'width:20%'}),

        }

class JourneyForm(ModelForm):
    start_time = MyDateTimeField(required=False)
    end_time = MyDateTimeField(required=False)

    class Meta:
        model = Journey
        fields = ['means_of_transport', 'name', 'start_point', 'end_point', 'start_time', 'end_time',
                  # 'date',
                  'price',
                  'more_info']
        widgets = {
            'means_of_transport': Select(attrs={'class': 'custom-select form-control-sm'}),
            'start_point': TextInput(attrs=dict_of_textinput_attrs_autocomplete),
            'end_point': TextInput(attrs=dict_of_textinput_attrs_autocomplete),
            'price': NumberInput(attrs=dict_of_textinput_attrs),
            'more_info': Textarea(
                attrs={'rows': 2, 'cols': '65', 'class': 'materialize-textarea form-control form-control-sm '
                                                         'more-info'}),
        }
        exclude = ('name',)


class AccommodationForm(ModelForm):
    date_range = MyDateRangeField(required=False)

    class Meta:
        model = Accommodation
        fields = ['name', 'address', 'date_range', 'price', 'more_info']
        widgets = {
            'name': TextInput(attrs=dict_of_textinput_attrs),
            'address': TextInput(attrs=dict_of_textinput_attrs),
            'price': NumberInput(attrs=dict_of_textinput_attrs),
            'more_info': Textarea(
                attrs={'rows': 2, 'cols': '65', 'class': 'materialize-textarea form-control form-control-sm more-info'}),
        }
        exclude = ()


class AttractionForm(ModelForm):
    start_time = MyDateTimeField(required=False)

    class Meta:
        model = Attraction
        fields = ['name', 'address', 'start_time', 'price', 'more_info']
        widgets = {
            'name': TextInput(attrs=dict_of_textinput_attrs),
            'address': TextInput(attrs=dict_of_textinput_attrs),
            'price': NumberInput(attrs=dict_of_textinput_attrs),
            'more_info': Textarea(
                attrs={'rows': 2, 'cols': '65', 'class': 'materialize-textarea form-control form-control-sm more-info'}),

        }
        exclude = ()



AttractionFormSet = inlineformset_factory(Trip, Attraction, form=AttractionForm, extra=1)
JourneyFormSet = inlineformset_factory(Trip, Journey, form=JourneyForm, extra=1)
AccommodationFormSet = inlineformset_factory(Trip, Accommodation, form=AccommodationForm, extra=1)


class ImageUploadForm(ModelForm):
    """Image upload form """

    class Meta:
        model = Trip
        fields = ['main_image']

    # def clean_main_image(self):
    #     main_image = self.cleaned_data.get('main_image', False)
    #     if main_image:
    #         if main_image._size > 2*1024*1024:
    #             raise ValidationError(_(str("Image file too large")))
            # return main_image
        # else:
        #     raise ValidationError(_(str("Couldn't read uploaded image")))



class ProfileForm(ModelForm, Form):
    class Meta:
        model = Profile
        fields = ['email', 'location','about_me' ]
        exclude = ()
        widgets = {
            'about_me': Textarea(attrs={'rows': '10', 'cols': '20', 'class': 'materialize-textarea form-control form-control-sm p-2'}),
            'location': TextInput(attrs=dict_of_textinput_attrs),
            'email': EmailInput(attrs=dict_of_textinput_attrs)

        }
