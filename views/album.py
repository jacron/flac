from django.http import HttpResponse
from django.template import loader
from ..db import (
    get_albums, get_album, get_pieces, get_componisten, get_performers,
    get_album_albums, get_album_performers, get_album_componisten, get_mother_title)
from ..services import get_cuesheet_title, get_cuesheet


def organize_pieces(items, album_path):
    cuesheets = []
    pieces = []
    for item in items:
        ffile = item[0].encode('utf-8')
        if ffile:
            extension = ffile.split('.')[-1]
            if extension == 'cue':
                if ffile == 'lijst.cue':
                    path = u'{}/{}'.format(album_path, ffile)
                    cuesheets.append(get_cuesheet_title(path, item[1]))
                else:
                    cuesheets.append(get_cuesheet(ffile, item[1]))
            else:
                pieces.append(item)
    return cuesheets, pieces


def album(request, album_id):
    template = loader.get_template('flac/album.html')
    album_o = get_album(album_id)
    mother_title = None
    if album_o['AlbumID']:
        mother_title = get_mother_title(album_o['AlbumID'])
    items = get_pieces(album_id)
    cuesheets, pieces = organize_pieces(items, album_o['Path'])

    context = {
        'items': pieces,
        'albums': get_album_albums(album_id),
        'album': album_o,
        'mother_title': mother_title,
        'componisten': get_componisten(),
        'album_componisten': get_album_componisten(album_id),
        'performers': get_performers(),
        'album_performers': get_album_performers(album_id),
        'cuesheet_output': cuesheets,
    }
    return HttpResponse(template.render(context, request))


def albums(request):
    template = loader.get_template('flac/albums.html')
    return HttpResponse(template.render(
        {
            'albums': get_albums(),
        }, request))
