from django.conf.urls import url
from .. import views

urlpatterns = [
    url(r'^(?P<componist_id>.+)/delete/$', views.componist_delete),
    url(r'^(?P<period>.+)/period/$', views.componisten_period),
    url(r'^(?P<componist_id>.+)/search/(?P<query>.+)/$',
        views.componist_search),
    url(r'^(?P<componist_id>.+)/$', views.componist, name='componist'),
    url(r'^$', views.componisten),
]