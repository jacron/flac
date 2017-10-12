from django.http import HttpResponse
from django.template import loader
from ..db import get_albums, get_album, get_pieces, get_performer, get_componist

def album(request, album_id):
    template = loader.get_template('flac/album.html')
    album_o = get_album(album_id)
    context = {
        'items': get_pieces(album_id),
        'album': album_o,
        'performer': get_performer(album_o['PerformerID']),
        'componist': get_componist(album_o['ComponistID'])
    }
    return HttpResponse(template.render(context, request))


def albums(request):
    template = loader.get_template('flac/albums.html')
    return HttpResponse(template.render(
        {
            'albums': get_albums(),
        }, request))
