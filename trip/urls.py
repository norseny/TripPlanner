from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.TripList.as_view(), name='trip-list'),
    url(r'trip/add/$', views.TripAttractionCreate.as_view(), name='trip-add'),
    url(r'trip/(?P<pk>[0-9]+)/$', views.TripAttractionUpdate.as_view(), name='trip-update'),
    url(r'trip/(?P<pk>[0-9]+)/delete/$', views.TripDelete.as_view(), name='trip-delete'),
]
