from django.http import HttpResponse
from django.template import loader

from flac.services import alfabet
from ..db import get_componist_albums, get_componisten, get_componist, get_period_componisten


def componist(request, componist_id):
    template = loader.get_template('flac/componist.html')
    context = {
        'items': get_componist_albums(componist_id),
        'componist': get_componist(componist_id),
    }
    return HttpResponse(template.render(context, request))


def componistenrequest(request, items, period=''):
    template = loader.get_template('flac/componisten.html')
    context = {
        'items': items,
        'letters': alfabet(),
        'period': period,
    }
    return HttpResponse(template.render(context, request))


def componisten_period(request, period):
    return componistenrequest(request, get_period_componisten(period), period)


def componisten_limited(request, min_limit):
    # obsolete
    return componistenrequest(request, get_componisten(min_limit))


def componisten(request):
    return componistenrequest(request, get_componisten())
