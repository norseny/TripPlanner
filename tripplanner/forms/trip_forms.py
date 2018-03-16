from django.forms import Form, ModelForm, inlineformset_factory, formset_factory, DateTimeInput


from tripplanner.models import *

class DateTimeInput(DateTimeInput):
    input_type = 'datetime'


class TripForm(ModelForm):
    class Meta:
        model = Trip
        exclude = ()



class AttractionForm(ModelForm):
    class Meta:
        model = Attraction
        exclude = ()


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


AttractionFormSet = inlineformset_factory(Trip, Attraction, form=AttractionForm, extra=1, max_num=10, min_num=0)
JourneyFormSet = inlineformset_factory(Trip, Journey, form=JourneyForm, extra=1)
AccomodationFormSet = inlineformset_factory(Trip, Accomodation, form=AccomodationForm, extra=1)

# AttractionFormSet = formset_factory(Attraction, extra=1)
