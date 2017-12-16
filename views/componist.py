from django.http import HttpResponse
from django.template import loader

from ..db import get_componist_albums, get_componisten, get_componist, get_period_componisten, \
    get_componist_albums_query, delete_componist


def componistrequest(request, componist_id, items, query=''):
    template = loader.get_template('flac/componist.html')
    context = {
        'items': items,
        'componist': get_componist(componist_id),
        'query': query,
    }
    return HttpResponse(template.render(context, request))


def componist_delete(request, componist_id):
    componist_o = get_componist(componist_id)
    delete_componist(componist_id)
    template = loader.get_template('flac/componist_deleted.html')
    return HttpResponse(template.render({'componist': componist_o}, request))


def componist(request, componist_id):
    return componistrequest(request, componist_id, get_componist_albums(componist_id))


def componistenrequest(request, items, period=''):
    template = loader.get_template('flac/componisten.html')
    context = {
        'items': items,
        'period': period,
    }
    return HttpResponse(template.render(context, request))


def componisten_period(request, period):
    return componistenrequest(request, get_period_componisten(period), period)


def componist_search(request, componist_id, query):
    return componistrequest(request, componist_id, get_componist_albums_query(componist_id, query), query)


def componisten(request):
    return componistenrequest(request, get_componisten())
