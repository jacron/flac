from django.http import HttpResponse
from django.template import loader

from flac.services import alfabet
from ..db import get_componist_albums, get_componisten, get_componist, get_period_componisten, \
    get_componist_albums_query


def componistrequest(request, componist_id, items, query=''):
    template = loader.get_template('flac/componist.html')
    context = {
        'items': items,
        'componist': get_componist(componist_id),
        'query': query,
    }
    return HttpResponse(template.render(context, request))


def componist(request, componist_id):
    return componistrequest(request, componist_id, get_componist_albums(componist_id))


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


def componist_search(request, componist_id, query):
    return componistrequest(request, componist_id, get_componist_albums_query(componist_id, query), query)


def componisten(request):
    return componistenrequest(request, get_componisten())
