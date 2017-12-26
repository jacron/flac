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
from django.conf.urls import url, include

# from flac.urls import componist as componist_urls
from .. import views

urlpatterns = [
    # url(r'^componist/', include(componist_urls)),
    url(r'^$', views.home),
    url(r'^home/$', views.home),

    url(r'^album/(?P<album_id>.+)/delete/$', views.album_delete),
    url(r'^album/(?P<album_id>.+)/(?P<list_name>.+)/(?P<list_id>.+)/$',
        views.album_list),
    url(r'^album/(?P<album_id>.+)/$', views.album),
    url(r'^album/$', views.albums),

    url(r'^performer/(?P<performer_id>.+)/delete/$', views.performer_delete),
    url(r'^performer/(?P<performer_id>.+)/$', views.performer),
    url(r'^performer/$', views.performers),

    url(r'^componist/(?P<componist_id>.+)/delete/$', views.componist_delete),
    url(r'^componist/(?P<period>.+)/period/$', views.componisten_period),
    url(r'^componist/(?P<componist_id>.+)/search/(?P<query>.+)/$',
        views.componist_search),
    url(r'^componist/(?P<componist_id>.+)/$', views.componist, name='componist'),
    url(r'^componist/$', views.componisten),

    url(r'^tag/(?P<tag_id>.+)/delete/$',
        views.tag_delete),
    url(r'^tag/(?P<tag_id>.+)/$',
        views.tag),
    url(r'^tag/$',
        views.tags),

    url(r'^instrument/(?P<instrument_id>.+)/delete/(?P<query>.+)/$',
        views.instrument_delete),
    url(r'^instrument/(?P<instrument_id>.+)/search/(?P<query>.+)/$',
        views.instrument_search),
    url(r'^instrument/(?P<instrument_id>.+)/$',
        views.instrument),
    url(r'^instrument/$',
        views.instrumenten),

    url(r'^extra/$',
        views.extra),
    url(r'^extra/(?P<cmd_code>.+)/$',
        views.cmd,
        name='cmd'),

    url(r'^librarycode/list/(?P<librarywild>.+)/$',
        views.list_librarycode,
        name='librarycodelist'),
    url(r'^librarycode/(?P<librarycode>.+)/(?P<librarywild>.+)/$',
        views.one_librarycode,
        name='librarycode'),
    url(r'^librarycode/(?P<librarycode>.+)/$',
        views.one_librarycode,
        name='librarycode'),

    url(r'^collection/(?P<query>.+)/search$', views.collections_search),
    url(r'^collection/$', views.collections),

    url(r'^ajax/$', views.ajax),
    url(r'^gather/$', views.gather),
    url(r'^gather/0/$', views.gather),

    url(r'^image/(?P<id>.+)/(?P<type>.+)/$', views.image),
    url(r'^imageback/(?P<id>.+)/(?P<type>.+)/$', views.imageback),

    url(r'^search/$', views.search),
    url(r'^search/(?P<query>.+)$',
        views.searchq,
        name='query'),

    url(r'^pianoboek/(?P<id>.+)/$', views.pianoboek),
    url(r'^pianoboek/$', views.pianoboeken),
    url(r'^upload/$', views.uploadalbum),
]
