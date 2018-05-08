from django.core.exceptions import PermissionDenied
from tripplanner.models import Trip
from django.contrib.auth.models import User


def user_is_trip_creator(function):
    def wrap(request, *args, **kwargs):
        trip = Trip.objects.get(pk=kwargs['pk'])
        if trip.created_by == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_trip_participant(function):
    def wrap(request, *args, **kwargs):
        curr_user = request.user.username

        trip = Trip.objects.get(pk=kwargs['pk'])
        if curr_user in list(trip.participants.values_list('username', flat=True).all()):

            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def trip_is_not_private(function):
    def wrap(request, *args, **kwargs):
        trip = Trip.objects.get(pk=kwargs['pk'])
        if trip.private_trip:
            if not trip.created_by == request.user:
                raise PermissionDenied
            else:
                return function(request, *args, **kwargs)
        else:
            return function(request, *args, **kwargs)


    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
