from django.http import HttpResponse
from django.template import loader
from ..db import (
    get_albums, get_album, get_pieces, get_componisten, get_performers, get_instruments,
    get_album_albums, get_album_performers, get_album_componisten, get_album_instruments,
    get_mother_title, get_tags, get_album_tags, )
from ..services import get_full_cuesheet


def organize_pieces(items, album_path):
    cuesheets = []
    pieces = []
    for item in items:
        ffile = item[0]
        if ffile:
            extension = ffile.split('.')[-1]
            if extension == 'cue':
                path = u'{}/{}'.format(album_path, ffile)
                try:
                    cuesheets.append(get_full_cuesheet(path, item[1]))
                except:
                    # path = '{}/{}'.format(album_path, ffile)
                    # cuesheets.append(get_full_cuesheet(path, item[1]))
                    print('could not get cuesheet for this path: ' + path)
            else:
                pieces.append(item)
    return cuesheets, pieces


def personslijst(items):
    # achternamen als label, maar bij ambivalentie aanvullen met voornaam
    out = []
    for item in items:
        out.append({
            "Title": item['FullName'],
            "Value": item['ID'],
            "Label": item['LastName'],
            "NameFull": item['NameFull']
        })
    doubles = []
    for obj in out:
        for obj2 in out:
            if obj2['Title'] != obj['Title'] and obj2['Label'] == obj['Label']:
                doubles.append(obj['Label'])
    for obj in out:
        if obj['Label'] in doubles:
            obj['Label'] = obj['NameFull']
    return out


def instrumentenlijst(items):
    out = []
    for item in items:
        out.append({
            "Title": '',
            "Value": item['ID'],
            "Label": item['Name'],
        })
    return out


def taglijst(items):
    out = []
    for item in items:
        out.append({
            "Title": '',
            "Value": item['ID'],
            "Label": item['Name'],
        })
    return out


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
        cuesheets = []
        pieces = []

    context = {
        'items': pieces,
        'albums': get_album_albums(album_id),
        'album': album_o,
        'mother_title': mother_title,
        'componisten': personslijst(get_componisten()),
        'album_componisten': get_album_componisten(album_id),
        'performers': personslijst(get_performers()),
        'album_performers': get_album_performers(album_id),
        'instrumenten': instrumentenlijst(get_instruments()),
        'album_instrument': get_album_instruments(album_id),
        'cuesheet_output': cuesheets,
        'tags': taglijst(get_tags()),
        'album_tags': get_album_tags(album_id),
    }
    return HttpResponse(template.render(context, request))


def albums(request):
    template = loader.get_template('flac/albums.html')
    return HttpResponse(template.render(
        {
            'albums': get_albums(),
        }, request))
