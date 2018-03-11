from django.urls import reverse_lazy

from django.db import transaction
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from trip.models import Trip
from trip.forms import AttractionFormSet


class TripList(ListView):
    model = Trip


class TripCreate(CreateView):
    model = Trip
    fields = ['name', 'description']


class TripAttractionCreate(CreateView):
    model = Trip
    fields = ['name', 'description']
    success_url = reverse_lazy('trip-list')

    def get_context_data(self, **kwargs):
        data = super(TripAttractionCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['attractions'] = AttractionFormSet(self.request.POST) #todo: takes only last line
        else:
            data['attractions'] = AttractionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        attractions = context['attractions']
        with transaction.atomic():
            if isinstance(form.instance, Trip):
                form.instance.created_by = self.request.user
            self.object = form.save()

            if attractions.is_valid():
                attractions.instance = self.object
                attractions.save()
        return super(TripAttractionCreate, self).form_valid(form)


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
