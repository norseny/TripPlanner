from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from tripplanner.decorators import user_is_trip_creator, user_is_trip_participant
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from tripplanner.forms import *
from tripplanner import models
from django.contrib.auth.models import User
from django.http import JsonResponse

from datetime import date
from io import BytesIO
from django.http import HttpResponse
from tripplanner.pdf_utils import PdfPrint
from django.contrib import messages

from django.utils.translation import gettext as _
from tripplanner import additional
from django.utils import timezone


group1 = [login_required, user_is_trip_creator]
group2 = [login_required, user_is_trip_participant]


class TripList(ListView):
    model = Trip

    def get_queryset(self):
        if self.request.user.is_authenticated:
            curr_user = User.objects.get(pk=self.request.user.id)
            return Trip.objects.exclude(participants=curr_user.id)
        else:
            return Trip.objects.all()

@method_decorator(login_required, name='dispatch')
class MyTripList(ListView):
    model = Trip
    template_name = 'tripplanner/my_trip_list.html'

    def get_queryset(self):
        curr_user = User.objects.get(pk=self.request.user.id)
        return Trip.objects.filter(participants=curr_user.id)


@method_decorator(login_required, name='dispatch')
class TripDetail(DetailView):
    model = Trip

    def get_context_data(self, **kwargs):
        trip = kwargs['object']
        all = list(trip.journey_set.all()) + list(trip.accommodation_set.all()) + list(trip.attraction_set.all())
        filtered_rows = [x for x in all if x.start_time != None]
        filtered_rows_leftouts = [x for x in all if x.start_time == None]
        filtered_rows.sort(key=lambda x: x.start_time)
        all_sorted = filtered_rows + filtered_rows_leftouts
        data = super(TripDetail, self).get_context_data(**kwargs)
        data['all'] = all_sorted
        try:
            if trip.participants.get(id=self.request.user.id):
                data['participant'] = True
        except:
            pass
        return data


@method_decorator(login_required, name='dispatch')
class TripWithAttributesCreate(CreateView):
    model = Trip
    form_class = TripForm
    template_name_suffix = '_with_attributes_form'

    def get_context_data(self, **kwargs):
        data = super(TripWithAttributesCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['journeys'] = JourneyFormSet(self.request.POST, )



            # to prevent default datetime_range to be saved later
            now = timezone.now().replace(hour=12, minute=00)
            now2 = timezone.now().replace(hour=11, minute=59)
            now = now.strftime('%d%m%Y%H%M')
            now2 = now2.strftime('%d%m%Y%H%M')

            for idx, el in enumerate(data['journeys'].cleaned_data):
                c = data['journeys'].cleaned_data[idx]['datetime_range']
                c0 = c[0].strftime('%d%m%Y%H%M')
                c1 = c[0].strftime('%d%m%Y%H%M')
                if (c0 == now) and ((c1 == now2) or (c1 == now)):
                    data['journeys'].cleaned_data[idx]['datetime_range'] = None



            data['accommodations'] = AccommodationFormSet(self.request.POST)
            data['attractions'] = AttractionFormSet(self.request.POST)
        else:
            data['journeys'] = JourneyFormSet()
            data['accommodations'] = AccommodationFormSet()
            data['attractions'] = AttractionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        journeys = context['journeys']
        accommodations = context['accommodations']
        attractions = context['attractions']
        with transaction.atomic():
            if attractions.is_valid() and accommodations.is_valid() and journeys.is_valid():
                current_user = self.request.user
                form.instance.created_by = current_user
                self.object = form.save()
                self.object.participants.add(current_user)

                if journeys.is_valid():

                    for el in journeys.cleaned_data:
                        if isinstance(el, dict):
                            if len(list((value for value in el.values() if value == None))) != 7: #dont allow to save
                                #  if all fields are empty
                                journeys.instance = self.object
                                journeys.save()

                                # save start_time and end_time from date_range
                                journeys_list = []
                                for element in self.object.journey_set.all():
                                    journeys_list.append(element.id)

                                for idx, el in enumerate(journeys.cleaned_data):
                                    if ('datetime_range' in el) and (el['DELETE'] == False):
                                        if len(journeys_list) >= idx+1:
                                            if el['datetime_range'] != None:
                                                journey = models.Journey.objects.get(pk=journeys_list[idx])
                                                journey.start_time = el['datetime_range'][0]
                                                journey.end_time = el['datetime_range'][1]
                                                journeys.cleaned_data[idx]['start_time'] = el['datetime_range'][0]
                                                journeys.cleaned_data[idx]['end_time'] = el['datetime_range'][1]
                                                journey.save()


                if accommodations.is_valid():
                    for el in journeys.cleaned_data:
                        if isinstance(el, dict):
                            if len(list((value for value in el.values() if value == None))) != 7: # if all fields are
                                #  empty
                                accommodations.instance = self.object
                                accommodations.save()

                if attractions.is_valid():
                    for el in journeys.cleaned_data:
                        if isinstance(el, dict):
                            if len(list((value for value in el.values() if value == None))) != 7: # if all fields are empty
                                attractions.instance = self.object
                                attractions.save()
                models.Trip.update_dates_and_price(self.object, journeys.cleaned_data, accommodations.cleaned_data,
                                                   attractions.cleaned_data)

            else:
                return self.form_invalid(form)

        return super(TripWithAttributesCreate, self).form_valid(form)


@method_decorator(group1, name='dispatch')
class TripWithAttributesUpdate(UpdateView):
    model = Trip
    form_class = TripForm
    template_name_suffix = '_with_attributes_form'

    def get_context_data(self, **kwargs):
        data = super(TripWithAttributesUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['journeys'] = JourneyFormSet(self.request.POST, instance=self.object)
            data['accommodations'] = AccommodationFormSet(self.request.POST, instance=self.object)
            data['attractions'] = AttractionFormSet(self.request.POST, instance=self.object)
        else:
            data['journeys'] = JourneyFormSet(instance=self.object)

            for idx, el in enumerate(data['journeys'].initial_forms):
                journey_id = data['journeys'].initial_forms[idx].instance.id
                journey = models.Journey.objects.get(pk=journey_id)
                if journey.start_time and journey.end_time:
                    datetime_range = additional.format_to_daterange(journey.start_time, journey.end_time)
                    data['journeys'].initial_forms[idx].initial['datetime_range'] = datetime_range

            data['accommodations'] = AccommodationFormSet(instance=self.object)
            data['attractions'] = AttractionFormSet(instance=self.object)
        return data


    def form_valid(self, form):
        context = self.get_context_data()
        journeys = context['journeys']
        accommodations = context['accommodations']
        attractions = context['attractions']
        with transaction.atomic():
            if attractions.is_valid() and accommodations.is_valid() and journeys.is_valid():
                form.instance.created_by = self.request.user
                self.object = form.save()

                if journeys.is_valid():
                    journeys.instance = self.object
                    journeys.save()

                    for idx, el in enumerate(journeys.cleaned_data):
                        if ('datetime_range' in el) and (el['DELETE'] == False):
                            if el['id']:
                                journey = models.Journey.objects.get(pk=el['id'].id)
                                journey.start_time = el['datetime_range'][0]
                                journeys.cleaned_data[idx]['start_time'] = el['datetime_range'][0]
                                journey.end_time = el['datetime_range'][1]
                                journeys.cleaned_data[idx]['end_time'] = el['datetime_range'][1]
                                journey.save()

                if accommodations.is_valid():
                    accommodations.instance = self.object
                    accommodations.save()
                if attractions.is_valid():
                    attractions.instance = self.object
                    attractions.save()
                models.Trip.update_dates_and_price(self.object, journeys.cleaned_data, accommodations.cleaned_data,
                                                   attractions.cleaned_data)
            else:
                return self.form_invalid(form)

        return super(TripWithAttributesUpdate, self).form_valid(form)


@method_decorator(group1, name='dispatch')
class TripDelete(DeleteView):
    model = Trip
    success_url = reverse_lazy('trip-list')


@method_decorator(login_required, name='dispatch')
class TripParticipantsList(FormView): # todo: change to list view, think of diff mechanism with adding and validation
    form_class = AddParticipantForm
    template_name = 'tripplanner/trip_participants_list.html'

    def get_success_url(self):
        return reverse_lazy('trip-participants', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        data = super(TripParticipantsList, self).get_context_data(**kwargs)
        data['trip'] = Trip.objects.get(id=self.kwargs['pk'])
        data['participants'] = Trip.objects.get(id=self.kwargs['pk']).participants.all()
        return data

    def form_valid(self, form):
        trip = Trip.objects.get(id=self.kwargs['pk'])
        user = User.objects.filter(username__iexact=form.cleaned_data['username']).first()
        trip.participants.add(user)

        return super(TripParticipantsList, self).form_valid(form)


def validate_participant(request):
    username = request.GET.get('username', None)
    trip_id = request.GET.get('tripId', None)
    trip = Trip.objects.get(pk=trip_id)
    success = False
    if User.objects.filter(username__iexact=username).exists():
        if username not in list(trip.participants.values_list('username', flat=True).all()):
            success = True
    data = {
        'exists': success,
        'message_error': _(str("User doesn't exist or is already added.")),
        'message_text': _(str('Click "Add" to add this user to your trip.'))
    }
    return JsonResponse(data)

def inspired(request):
    user_id = request.user.id
    trip_id = request.GET.get('tripId', None)
    trip_org = Trip.objects.get(pk=trip_id)
    trip_clone = Trip.objects.get(pk=trip_id)

    try:
        trip_clone.name = trip_clone.name + ' copy'
        trip_clone.created_by_id = user_id
        trip_clone.start_time = None
        trip_clone.end_time = None
        trip_clone.price = None
        trip_clone.pk = None
        trip_clone.save()
        trip_clone.participants.add(request.user)

        for journey in trip_org.journey_set.all():
            journey_clone = journey
            journey_clone.start_time = None
            journey_clone.end_time = None
            journey_clone.price = None
            journey_clone.pk = None
            journey_clone.trip_id = trip_clone.id
            journey_clone.save()

        for accommodation in trip_org.accommodation_set.all():
            accommodation_clone = accommodation
            accommodation_clone.start_time = None
            accommodation_clone.end_time = None
            accommodation_clone.price = None
            accommodation_clone.pk = None
            accommodation_clone.trip_id = trip_clone.id
            accommodation_clone.save()

        for attraction in trip_org.attraction_set.all():
            attraction_clone = attraction
            attraction_clone.start_time = None
            attraction_clone.end_time = None
            attraction_clone.price = None
            attraction_clone.pk = None
            attraction_clone.trip_id = trip_clone.id
            attraction_clone.save()

        messages.success(request, _('Here is your new trip! Change the name and fill in some fields.'))

        data = {
             'tripEditUrl': reverse_lazy('trip-update',
                                kwargs={'pk': trip_clone.id}),
         }
    except:
        pass #todo: sth...

    return JsonResponse(data)


@method_decorator(group2, name='dispatch')
class TripDetailPdf(DetailView):
    model = Trip

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='application/pdf')
        today = date.today()
        filename = _(context['trip'].name) + '_' + today.strftime('%d-%m-%Y')
        response['Content-Disposition'] = \
            'attachement; filename={0}.pdf'.format(filename)
        buffer = BytesIO()
        print = PdfPrint(buffer, 'A4')
        pdf = print.report(context, context['trip'].name)
        response.write(pdf)
        return response


@method_decorator(group2, name='dispatch')
class ImageUploadView(UpdateView):
    model = Trip
    form_class = ImageUploadForm
    template_name = 'tripplanner/trip_upload_img.html'
