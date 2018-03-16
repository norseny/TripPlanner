from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, FormView
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory

from tripplanner.models import *
from tripplanner.forms import *


class TripList(ListView):
    model = Trip


class TripDetail(DetailView):
    model = Trip


class TripCreate(CreateView):
    model = Trip
    template_name_suffix = '_create_form'
    fields = ['name', 'description', 'start_time', 'end_time']

    def get_success_url(self):
        return reverse('trip-add-attraction', kwargs={'trip_id': self.object.id})

    def form_valid(self, form):
        with transaction.atomic():
            if isinstance(form.instance, Trip):
                form.instance.created_by = self.request.user
                self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())


# class TripAttractionCreate(FormView):
#     form_class = modelformset_factory(
#         Attraction,
#         fields=['place', 'start_time', 'end_time','price'],
#         max_num=10,
#         can_delete=True
#     )
#     success_url = reverse_lazy('trip-list') # todo: do accomodation/journey
#     template_name = 'tripplanner/attraction_trip_create_form.html'
#
#     def get_form_kwargs(self):
#         kwargs = super(TripAttractionCreate, self).get_form_kwargs()
#         kwargs["queryset"] = Attraction.objects.none()
#         return kwargs
#
#     def form_valid(self, form):
#         for sub_form in form:
#             if sub_form.has_changed():
#                 sub_form.instance.trip_id = self.kwargs['trip_id']
#                 sub_form.save()
#
#         return super(TripAttractionCreate, self).form_valid(form)


class TripWithAttributesCreate(CreateView):
    model = Trip
    fields = ['name', 'description']#'start_time', 'end_time']
    success_url = reverse_lazy('trip-list')  # todo:
    template_name_suffix = '_with_attributes_form'
    # template_name = 'tripplanner/trip_with_attr_form.html'

    def get_context_data(self, **kwargs):
        data = super(TripWithAttributesCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['journeys'] = JourneyFormSet(self.request.POST)
            data['accomodations'] = AccomodationFormSet(self.request.POST)
            data['attractions'] = AttractionFormSet(self.request.POST)
        else:
            data['journeys'] = JourneyFormSet()
            data['accomodations'] = AccomodationFormSet()
            data['attractions'] = AttractionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        journeys = context['journeys']
        accomodation = context['accomodations']
        attractions = context['attractions']
        with transaction.atomic():
            self.object = form.save()

            if journeys.is_valid():
                journeys.instance = self.object
                journeys.save()
            if accomodation.is_valid():
                accomodation.instance = self.object
                accomodation.save()
            if attractions.is_valid():
                attractions.instance = self.object
                attractions.save()

        return super(TripWithAttributesCreate, self).form_valid(form)


class TripUpdate(UpdateView):
    model = Trip
    success_url = '/'
    fields = ['name', 'description']


class TripAttractionUpdate(UpdateView):
    model = Trip
    fields = ['name', 'description']
    success_url = reverse_lazy('trip-list')

    def get_context_data(self, **kwargs):
        data = super(TripAttractionUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['attractions'] = AttractionFormSet(self.request.POST, instance=self.object)
        else:
            data['attractions'] = AttractionFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        attractions = context['attractions']
        with transaction.atomic():
            self.object = form.save()

            if attractions.is_valid():
                attractions.instance = self.object
                attractions.save()
        return super(TripAttractionUpdate, self).form_valid(form)


class TripDelete(DeleteView):
    model = Trip
    success_url = reverse_lazy('trip-list')
