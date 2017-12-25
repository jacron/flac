from django.http import HttpResponse
from django.template import loader

from flac import settings
from ..db import get_componist_albums, get_componisten, get_componist, get_period_componisten, \
    get_componist_albums_query, delete_componist, get_performer_path, get_componist_path

import os


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


def has_image(person_id):
    person_path = get_componist_path(person_id)
    if person_path:
        image_path = person_path + settings.PERSON_FILE
        return os.path.exists(image_path)
    return False


def componisten(request):
    componisten = get_componisten()
    for person in componisten:
        person['has_image'] = has_image(person['ID'])
    return componistenrequest(request, componisten)
