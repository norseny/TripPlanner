from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from tripplanner import views


urlpatterns = [
    url(r'^$', login_required(views.TripList.as_view()), name='trip-list'),
    url(r'trip/(?P<pk>[0-9]+)/$', login_required(views.TripDetail.as_view()), name='trip-detail'),
    # url(r'trip/add/$', login_required(views.TripCreate.as_view()), name='trip-add'),
    url(r'trip/create/$', login_required(views.TripWithAttributesCreate.as_view()), name='trip-with-attributes-create'),
    url(r'trip/(?P<pk>[0-9]+)/edit/$', login_required(views.TripWithAttributesUpdate.as_view()), name='trip-update'),
    url(r'trip/(?P<pk>[0-9]+)/delete/$', login_required(views.TripDelete.as_view()), name='trip-delete'),
]
