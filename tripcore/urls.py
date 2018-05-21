"""trip-core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponseRedirect
from tripplanner import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
import tripcore

urlpatterns = [
    url(r'^tripplanner/', include('tripplanner.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('tripplanner.urls')),
    url(r'^$', lambda r: HttpResponseRedirect('tripplanner/')),
    url(r'^login/$', auth_views.login, {'template_name': 'register/login.html'}, name='login'),
    url(r'^logout/$', login_required(auth_views.logout), {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url('i18n/', include('django.conf.urls.i18n')),
] + static(tripcore.settings.MEDIA_URL, document_root=tripcore.settings.MEDIA_ROOT)