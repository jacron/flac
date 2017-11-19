from django.http import HttpResponse
from django.template import loader

from flac.db import get_albums
from flac.services.album_content import album_context


def album_list(request, album_id, list_id, list_name):
    template = loader.get_template('flac/album.html')
    context = album_context(album_id, list_name, list_id)
    if not context:
        return HttpResponse()
    return HttpResponse(template.render(context, request))


def album(request, album_id):
    template = loader.get_template('flac/album.html')
    context = album_context(album_id)
    if not context:
        return HttpResponse()
    return HttpResponse(template.render(context, request))


def albums(request):
    template = loader.get_template('flac/albums.html')
    return HttpResponse(template.render(
        {'albums': get_albums(), }, request))
