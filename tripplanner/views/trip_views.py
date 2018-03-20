from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from tripplanner.forms import *


class TripList(ListView):
    model = Trip


class TripDetail(DetailView):
    model = Trip


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
        accommodation = context['accommodations']
        attractions = context['attractions']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()

            if journeys.is_valid():
                journeys.instance = self.object
                journeys.save()
            else:
                return self.form_invalid(form)
            if accommodation.is_valid():
                accommodation.instance = self.object
                accommodation.save()
            else:
                return self.form_invalid(form)
            if attractions.is_valid():
                attractions.instance = self.object
                attractions.save()
            else:
                return self.form_invalid(form)

            # todo: check and update trip: full cost, start and end date

        return super(TripWithAttributesCreate, self).form_valid(form)


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
        accommodation = context['accommodations']
        attractions = context['attractions']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()

            if journeys.is_valid():
                journeys.instance = self.object
                journeys.save()
            else:
                return self.form_invalid(form)
            if accommodation.is_valid():
                accommodation.instance = self.object
                accommodation.save()
            else:
                return self.form_invalid(form)
            if attractions.is_valid():
                attractions.instance = self.object
                attractions.save()
            else:
                return self.form_invalid(form)


        return super(TripWithAttributesUpdate, self).form_valid(form)


class TripDelete(DeleteView):
    model = Trip
    success_url = reverse_lazy('trip-list')
