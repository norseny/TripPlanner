from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from trip import views


urlpatterns = [
    url(r'^$', login_required(views.TripList.as_view()), name='trip-list'),
    url(r'trip/add/$', login_required(views.TripAttractionCreate.as_view()), name='trip-add'),
    url(r'trip/(?P<pk>[0-9]+)/$', login_required(views.TripAttractionUpdate.as_view()), name='trip-update'),
    url(r'trip/(?P<pk>[0-9]+)/delete/$', login_required(views.TripDelete.as_view()), name='trip-delete'),
]
