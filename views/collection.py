from django.http import HttpResponse
from django.template import loader
from ..db import (get_collections, get_collections_query)


def collections(request):
    template = loader.get_template('flac/collections.html')
    ccollections = get_collections()
    return HttpResponse(template.render(
        {
            'albums': ccollections
        }, request))


def collections_search(request, query):
    template = loader.get_template('flac/collections.html')
    ccollections = get_collections_query(query)
    return HttpResponse(template.render(
        {
            'albums': ccollections,
            'query': query
        }, request))
