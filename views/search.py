from django.http import HttpResponse
from django.template import loader

from flac.db import get_albums_by_title, get_albums_by_cql, get_componist, get_performer, get_tag, get_instrument


def searchresponse(context, request):
    template = loader.get_template('flac/search.html')
    return HttpResponse(template.render(context, request))


def searchq(request, query):
    context = {
            'query': query,
            'albums': get_albums_by_title(query)
        }
    return searchresponse(context, request)


def get_item_name(request, type):
    if request.GET.get(type):
        type_id = request.GET.get(type)
        if type == 'componist':
            componist = get_componist(type_id)
            return '{}_{}'.format(componist['FullName'], componist['ID'])
        if type == 'performer':
            performer = get_performer(type_id)
            return '{}_{}'.format(performer['FullName'], performer['ID'])
        if type == 'tag':
            tag = get_tag(type_id)
            return '{}_{}'.format(tag['Name'], tag['ID'])
        if type == 'instrument':
            instrument = get_instrument(type_id)
            return '{}_{}'.format(instrument['Name'], instrument['ID'])
    return ''


def search(request):
    albums = get_albums_by_cql(request.GET)
    return searchresponse({
        'albums': albums,
        'mothers': albums.get('mothers'),
        'children': albums.get('children'),
        # 'componist_name': get_item_name(request, 'componist'),
        # 'performer_name': get_item_name(request, 'performer'),
        # 'tag_name': get_item_name(request, 'tag'),
        # 'instrument_name': get_item_name(request, 'instrument'),
    }, request)
