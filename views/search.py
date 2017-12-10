from django.http import HttpResponse
from django.template import loader

from flac.db import get_albums_by_title, get_albums_by_cql


def searchresponse(context, request):
    template = loader.get_template('flac/searchq.html')
    return HttpResponse(template.render(context, request))


def searchq(request, query):
    context = {
            'query': query,
            'albums': get_albums_by_title(query)
        }
    return searchresponse(context, request)


def search(request):
    albums = get_albums_by_cql(request.GET)
    return searchresponse({
        'albums': albums,
        'mothers': albums['mothers'],
        'children': albums['children'],
    }, request)
