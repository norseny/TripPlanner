from django.core.exceptions import PermissionDenied
from tripplanner.models import Trip
from django.contrib.auth.models import User


def user_is_admin_or_trip_creator(function):
    def wrap(request, *args, **kwargs):
        curr_user = User.objects.get(pk=request.user.id)
        if not curr_user.is_superuser:
            trip = Trip.objects.get(pk=kwargs['pk'])
            if trip.created_by == request.user:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap