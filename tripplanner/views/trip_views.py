from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from tripplanner.decorators import user_is_admin_or_trip_creator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from tripplanner.forms import *
from tripplanner import models

# import pdfkit
# from django.http import HttpResponse

decorators = [login_required, user_is_admin_or_trip_creator]


class TripList(ListView):
    model = Trip

    def get_queryset(self):
        curr_user = User.objects.get(pk=self.request.user.id)
        if not curr_user.is_superuser:
            return Trip.objects.filter(created_by=self.request.user.pk)
        else:
            return Trip.objects.all()


@method_decorator(decorators, name='dispatch')
class TripDetail(DetailView):
    model = Trip


@method_decorator(login_required, name='dispatch')
class TripWithAttributesCreate(CreateView):
    model = Trip
    form_class = TripForm
    template_name_suffix = '_with_attributes_form'

    def get_context_data(self, **kwargs):
        data = super(TripWithAttributesCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['journeys'] = JourneyFormSet(self.request.POST, )
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
                form.instance.created_by = self.request.user
                self.object = form.save()

                if journeys.is_valid():
                    journeys.instance = self.object
                    journeys.save()
                if accommodations.is_valid():
                    accommodations.instance = self.object
                    accommodations.save()
                if attractions.is_valid():
                    attractions.instance = self.object
                    attractions.save()
                models.Trip.update_dates_and_price(self.object, journeys, accommodations, attractions) # todo:
                # sprawdzic czy dzialaja daty - wprowadzanie
            else:
                return self.form_invalid(form)

        return super(TripWithAttributesCreate, self).form_valid(form)


@method_decorator(decorators, name='dispatch')
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
                if accommodations.is_valid():
                    accommodations.instance = self.object
                    accommodations.save()
                if attractions.is_valid():
                    attractions.instance = self.object
                    attractions.save()
                models.Trip.update_dates_and_price(self.object, journeys.cleaned_data, accommodations.cleaned_data, attractions.cleaned_data)
            else:
                return self.form_invalid(form)

        return super(TripWithAttributesUpdate, self).form_valid(form)


@method_decorator(decorators, name='dispatch')
class TripDelete(DeleteView):
    model = Trip
    success_url = reverse_lazy('trip-list')

#
# def pdffile(request):
#
#     # pdf = pdfkit.from_url("http://localhost:8001/trip/1/", "trip1.pdf")
#     # return HttpResponse("Everything working good, check out the root of your project to see the generated PDF.")
#
#     # Use False instead of output path to save pdf to a variable
#     pdf = pdfkit.from_url('http://localhost:8001/tripplanner/published-trip', False)
#     response = HttpResponse(pdf,content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="trip1.pdf"'
#
#
#     return response
