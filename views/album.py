# import unidecode as unidecode
from unidecode import unidecode

from django.http import HttpResponse
from django.template import loader
from ..db import (
    get_albums, get_album, get_pieces, get_setting, get_next_album, get_prev_album, get_componisten, get_performers,
    get_mother_title, get_album_albums, get_album_componisten, get_album_performers, get_album_instruments,
    get_album_tags)
from ..services import get_full_cuesheet


def hasPerson(s, persons):
    proposals = []
    if s is None:
        return []
    s = s.replace('_', ' ')
    try:
        s = unidecode(s.upper())
    except Exception:
        s = s.upper()
    for person in persons:
        p = unidecode(person['LastName'].upper())
        if len(p) > 2 and p in s:
            proposals.append(person)
    return proposals


def ontdubbel(persons):
    npersons = []
    for person in persons:
        if person not in npersons:
            npersons.append(person)
    return npersons


def get_proposals(cuesheets, album_title):
    componisten = get_componisten()
    proposals = []
    for cuesheet in cuesheets:
        proposals = proposals + hasPerson(cuesheet['Title'], componisten)
        proposals = proposals + hasPerson(cuesheet['Filename'], componisten)
    proposals = proposals + hasPerson(album_title, componisten)
    return ontdubbel(proposals)


def get_artists(cuesheets, album_title):
    performers = get_performers()
    proposals = []
    for cuesheet in cuesheets:
        proposals = proposals + hasPerson(cuesheet['Title'], performers)
        proposals = proposals + hasPerson(cuesheet['Filename'], performers)
    proposals = proposals + hasPerson(album_title, performers)
    return ontdubbel(proposals)


def organize_pieces(album_id, album_path):
    items = get_pieces(album_id)
    cuesheets = []
    pieces = []
    read_cuesheet_setting = get_setting('read_cuesheet')
    read_cuesheet = read_cuesheet_setting['VALUE'] == '1'
    print(read_cuesheet)
    for item in items:
        ffile = item[0]
        if ffile:
            extension = ffile.split('.')[-1]
            if extension == 'cue':
                if read_cuesheet:
                    path = u'{}/{}'.format(album_path, ffile)
                    try:
                        cuesheets.append(get_full_cuesheet(path, item[1]))
                    except Exception:
                        pass
            else:
                pieces.append(item)
    return cuesheets, pieces


def album_next(request, album_id):
    template = loader.get_template('flac/album.html')
    album_o = get_album(album_id)
    if album_o['AlbumID']:
        next_id = get_next_album(album_o['AlbumID'], album_id)
        if next_id:
            album_id = next_id
    context = album_context(album_id)
    return HttpResponse(template.render(context, request))


def album_prev(request, album_id):
    template = loader.get_template('flac/album.html')
    album_o = get_album(album_id)
    if album_o['AlbumID']:
        prev_id = get_prev_album(album_o['AlbumID'], album_id)
        if prev_id:
            album_id = prev_id
    context = album_context(album_id)
    return HttpResponse(template.render(context, request))


def album_context(album_id):
    album_o = get_album(album_id)
    if not album_o:
        return None

    mother_title = None
    cuesheets, pieces, proposals, artists = [], [], [], []
    album_o = get_album(album_id)
    if album_o['AlbumID']:
        mother_title = get_mother_title(album_o['AlbumID'])
        cuesheets, pieces = organize_pieces(album_id, album_o['Path'])
        proposals = get_proposals(cuesheets, album_o['Title'])
        artists = get_artists(cuesheets, album_o['Title'])
    return {
        'albumid': album_id,
        'items': pieces,
        'albums': get_album_albums(album_id),
        'album': album_o,
        'mother_title': mother_title,
        'album_componisten': get_album_componisten(album_id),
        'album_performers': get_album_performers(album_id),
        'album_instrument': get_album_instruments(album_id),
        'cuesheet_output': cuesheets,
        'album_tags': get_album_tags(album_id),
        'proposals': proposals,
        'artists': artists,
    }


def album(request, album_id):
    template = loader.get_template('flac/album.html')
    context = album_context(album_id)
    if not context:
        return HttpResponse()
    return HttpResponse(template.render(context, request))


def albums(request):
    template = loader.get_template('flac/albums.html')
    return HttpResponse(template.render(
        {
            'albums': get_albums(),
        }, request))
