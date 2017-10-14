from django.http import HttpResponse
from django.template import loader
from ..db import (
    get_collections, get_album, )


def collections(request):
    template = loader.get_template('flac/collections.html')
    collections = get_collections()
    return HttpResponse(template.render(
        {
            'albums': collections
        }, request))


def collection(request, collection_id):
    album_o = get_album(collection_id)
    template = loader.get_template('flac/collection.html')
    pass