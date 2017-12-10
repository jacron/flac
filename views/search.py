from django.http import HttpResponse
from django.template import loader

from flac.db import get_albums_by_title, get_albums_by_cql, get_componist


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
    # componist_name = None
    # componist = get_componist(request.GET.get('componist'))
    # if componist:
    #     componist_name = componist['FullName']
        # componist_name = '{}_{}'.format(componist['FullName'], componist['ID'])
    return searchresponse({
        'albums': albums,
        'mothers': albums.get('mothers'),
        'children': albums.get('children'),
        # 'componist_name': componist_name
    }, request)
