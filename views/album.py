from django.http import HttpResponse
from django.template import loader

from flac.db import get_next_album, get_prev_album, get_albums
from flac.services.album_content import album_context


def album(request, album_id):
    template = loader.get_template('flac/album.html')
    context = album_context(album_id)
    if not context:
        return HttpResponse()
    prev_id = get_prev_album(context['album']['AlbumID'], album_id)
    next_id = get_next_album(context['album']['AlbumID'], album_id)
    context['prev_id'] = prev_id
    context['next_id'] = next_id
    return HttpResponse(template.render(context, request))


def albums(request):
    template = loader.get_template('flac/albums.html')
    return HttpResponse(template.render(
        {'albums': get_albums(), }, request))
