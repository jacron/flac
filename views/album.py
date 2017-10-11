from django.http import HttpResponse
from django.template import loader
from ..db import get_albums, get_album, get_pieces


def album(request, album_id):
    template = loader.get_template('flac/album.html')

    context = {
        'items': get_pieces(album_id),
        'album': get_album(album_id),
    }
    return HttpResponse(template.render(context, request))


def albums(request):
    template = loader.get_template('flac/albums.html')
    return HttpResponse(template.render(
        {
            'albums': get_albums(),
         }, request))
