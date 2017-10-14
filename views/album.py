# from cueparser import CueSheet
from django.http import HttpResponse
from django.template import loader
from ..db import get_albums, get_album, get_pieces, get_componist, get_album_albums, get_album_performers
from ..services import get_cuesheet


def album(request, album_id):
    template = loader.get_template('flac/album.html')
    album_o = get_album(album_id)
    items = get_pieces(album_id)
    cuesheets = []
    pieces = []
    for item in items:
        file = item[0]
        if file:
            extension = file.split('.')[-1]
            if extension == 'cue':
                path = '{}/{}'.format(album_o['Path'], file)
                cuesheets.append(get_cuesheet(path, item[1]))
            else:
                pieces.append(item)

    context = {
        'items': pieces,
        'albums': get_album_albums(album_id),
        'album': album_o,
        'componist': get_componist(album_o['ComponistID']),
        'performers': get_album_performers(album_id),
        'cuesheet_output': cuesheets
    }
    return HttpResponse(template.render(context, request))


def albums(request):
    template = loader.get_template('flac/albums.html')
    return HttpResponse(template.render(
        {
            'albums': get_albums(),
        }, request))
