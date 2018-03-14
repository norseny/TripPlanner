from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, FormView
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory

from tripplanner.models import *
from tripplanner.forms import AttractionFormSet

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


class TripAttractionCreate(FormView):
    form_class = modelformset_factory(
        Attraction,
        fields=['price', 'place', 'start_time', 'end_time'],
        extra=3
    )
    success_url = reverse_lazy('trip-list') #todo: do accomodation/journey
    template_name = 'tripplanner/attraction_trip_create_form.html'

    def get_form_kwargs(self):
        kwargs = super(TripAttractionCreate, self).get_form_kwargs()
        kwargs["queryset"] = Attraction.objects.none()
        return kwargs

    def form_valid(self, form):
        for sub_form in form:
            if sub_form.has_changed():
                sub_form.save()

        return super(TripAttractionCreate, self).form_valid(form)


#
# class TripAttractionCreate(CreateView):
#     model = Trip
#     fields = ['name', 'description']
#     success_url = reverse_lazy('trip-list')
#
#     def get_context_data(self, **kwargs):
#         data = super(TripAttractionCreate, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['attractions'] = AttractionFormSet(self.request.POST)  # todo: takes only last line
#         else:
#             data['attractions'] = AttractionFormSet()
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         attractions = context['attractions']
#         with transaction.atomic():
#             if isinstance(form.instance, Trip):
#                 form.instance.created_by = self.request.user
#                 self.object = form.save()
#
#             if attractions.is_valid():
#                 attractions.instance = self.object
#                 attractions.save()
#         return super(TripAttractionCreate, self).form_valid(form)


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
