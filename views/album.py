from django.http import HttpResponse
from django.template import loader
from ..db import (
    get_albums, get_album, get_pieces, get_componisten, get_performers, get_instruments,
    get_album_albums, get_album_performers, get_album_componisten, get_album_instruments,
    get_mother_title, get_tags, get_album_tags, )
from ..services import get_full_cuesheet, get_cuesheet


def organize_pieces(items, album_path):
    cuesheets = []
    pieces = []
    for item in items:
        try:
            ffile = item[0].encode('utf-8')
        except:
            ffile = item[0]
            print("could not encode filename:" + ffile)
        if ffile:
            extension = ffile.split('.')[-1]
            if extension == 'cue':
                try:
                    # sometimes prefixing with 'u' seems necessary but then reading the file will fail
                    path = '{}/{}'.format(album_path, ffile)
                    cuesheets.append(get_full_cuesheet(path, item[1]))
                except:
                    # path = '{}/{}'.format(album_path, ffile)
                    # cuesheets.append(get_full_cuesheet(path, item[1]))
                    print('could not get cuesheet for this path: ' + path)
            else:
                pieces.append(item)
    return cuesheets, pieces


def album(request, album_id):
    template = loader.get_template('flac/album.html')
    album_o = get_album(album_id)
    if not album_o:
        return HttpResponse()

    mother_title = None
    if album_o['AlbumID']:
        mother_title = get_mother_title(album_o['AlbumID'])
    try:
        items = get_pieces(album_id)
        cuesheets, pieces = organize_pieces(items, album_o['Path'])
    except:
        print('Cannot get pieces')

    context = {
        'items': pieces,
        'albums': get_album_albums(album_id),
        'album': album_o,
        'mother_title': mother_title,
        'componisten': get_componisten(),
        'album_componisten': get_album_componisten(album_id),
        'performers': get_performers(),
        'album_performers': get_album_performers(album_id),
        'instrumenten': get_instruments(),
        'album_instrument': get_album_instruments(album_id),
        'cuesheet_output': cuesheets,
        'tags': get_tags(),
        'album_tags': get_album_tags(album_id),
    }
    return HttpResponse(template.render(context, request))


def albums(request):
    template = loader.get_template('flac/albums.html')
    return HttpResponse(template.render(
        {
            'albums': get_albums(),
        }, request))
