# import unidecode as unidecode
from unidecode import unidecode

from django.http import HttpResponse
from django.template import loader
from ..db import (
    get_albums, get_album, get_pieces, get_setting, get_next_album, get_prev_album, get_componisten, get_performers)
from ..services import get_full_cuesheet


def hasPerson(s, persons):
    proposals = []
    s = unidecode(s.upper())
    for person in persons:
        p = unidecode(person['LastName'].upper())
        if p in s:
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
    proposals = proposals + hasPerson(album_title, componisten)
    return ontdubbel(proposals)


def get_artists(cuesheets, album_title):
    performers = get_performers()
    proposals = []
    for cuesheet in cuesheets:
        proposals = proposals + hasPerson(cuesheet['Title'], performers)
    proposals = proposals + hasPerson(album_title, performers)
    return ontdubbel(proposals)


def organize_pieces(album_id, album_path):
    items = get_pieces(album_id)
    cuesheets = []
    pieces = []
    read_cuesheet = get_setting('read_cuesheet')
    print(read_cuesheet['VALUE'])
    for item in items:
        ffile = item[0]
        if ffile:
            extension = ffile.split('.')[-1]
            if extension == 'cue':
                if int(read_cuesheet['VALUE']) == 1:
                    path = u'{}/{}'.format(album_path, ffile)
                    try:
                        cuesheets.append(get_full_cuesheet(path, item[1]))
                    except:
                        print('could not get cuesheet for this path: ' + path)
            else:
                pieces.append(item)
    return cuesheets, pieces


def album_next(request, album_id):
    template = loader.get_template('flac/album.html')
    album_o = get_album(album_id)
    if album_o['AlbumID']:
        next_id = get_next_album(album_o['AlbumID'], album_id)
        if next_id:
            album_o = get_album(next_id)
    context = {
        'album': album_o,
    }
    return HttpResponse(template.render(context, request))


def album_prev(request, album_id):
    template = loader.get_template('flac/album.html')
    album_o = get_album(album_id)
    if album_o['AlbumID']:
        prev_id = get_prev_album(album_o['AlbumID'], album_id)
        if prev_id:
            album_o = get_album(prev_id)
    context = {
        'album': album_o,
    }
    return HttpResponse(template.render(context, request))


def album(request, album_id):
    template = loader.get_template('flac/album.html')
    album_o = get_album(album_id)
    if not album_o:
        return HttpResponse()

    context = {
        'album': album_o,
    }
    return HttpResponse(template.render(context, request))


def albums(request):
    template = loader.get_template('flac/albums.html')
    return HttpResponse(template.render(
        {
            'albums': get_albums(),
        }, request))
