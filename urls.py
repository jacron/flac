"""flac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home/$', views.home),
    url(r'^album/(?P<album_id>.+)/$', views.album),
    url(r'^album/$', views.albums),
    url(r'^performer/(?P<performer_id>.+)/$', views.performer),
    url(r'^performer/$', views.performers),
    url(r'^componist/(?P<componist_id>.+)/$', views.componist),
    url(r'^componist/$', views.componisten),
    url(r'^instrument/(?P<instrument_id>.+)/$', views.instrument),
    url(r'^instrument/$', views.instrumenten),
    url(r'^ajax/$', views.ajax),
    url(r'^albumimage/(?P<album_id>.+)/$', views.albumimage),
    url(r'^componistimage/(?P<componist_id>.+)/$', views.componistimage),
]
