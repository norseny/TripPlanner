from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from tripplanner import views
from tripcore import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.tripplanner, name='tripplanner'),
    url(r'^trips$', (views.TripList.as_view()), name='trip-list'),
    url(r'my-trips$', (views.MyTripList.as_view()), name='my-trip-list'),
    url(r'trip/(?P<pk>[0-9]+)/$', views.TripDetail.as_view(), name='trip-detail'),
    url(r'trip/create/$', views.TripWithAttributesCreate.as_view(), name='trip-with-attributes-create'),
    url(r'trip/(?P<pk>[0-9]+)/edit/$', views.TripWithAttributesUpdate.as_view(), name='trip-update'),
    url(r'trip/(?P<pk>[0-9]+)/delete/$', views.TripDelete.as_view(), name='trip-delete'),
    url(r'trip/(?P<pk>[0-9]+)/participants$', views.TripParticipantsList.as_view(), name='trip-participants'),
    url(r'^ajax/validate-participant/$', views.validate_participant, name='validate-participant'),
    url(r'^ajax/add-participant/$', views.add_participant, name='add-participant'),
    url(r'^ajax/remove-participant/$', views.remove_participant, name='remove-participant'),
    url(r'^ajax/inspired/$', views.inspired, name='inspired'),
    url(r'trip/(?P<pk>[0-9]+)/pdf$', views.TripDetailPdf.as_view(), name='trip-detail-pdf'),
    url(r'trip/(?P<pk>[0-9]+)/upload-img$', views.ImageUploadView.as_view(), name='upload-trip-img'),
    url(r'^autocomplete/get_places/', views.get_places, name='get-places'),
] \
              # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #todo: sort it out
