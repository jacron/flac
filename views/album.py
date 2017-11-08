# import unidecode as unidecode
import os
from unidecode import unidecode

from django.http import HttpResponse
from django.template import loader
from ..db import (
    get_albums, get_album, get_pieces, get_next_album, get_prev_album, get_componisten, get_performers,
    get_mother_title, get_album_albums, get_album_componisten, get_album_performers, get_album_instruments,
    get_album_tags, get_componist, get_componist_aliasses, get_performer_aliasses, get_performer, get_setting)
from ..services import get_full_cuesheet


def has_alias(s, persons, id_field):
    proposals = []
    if s is None:
        return []
    s = s.replace('_', ' ')
    try:
        s = unidecode(s.upper())
    except Exception:
        s = s.upper()
    for person in persons:
        p = unidecode(person['Name'].upper())
        if len(p) > 2 and p in s:
            if id_field == 'ComponistID':
                fperson = get_componist(person[id_field])
            else:
                fperson = get_performer(person[id_field])
            proposals.append(fperson)
    return proposals


def has_person(s, persons):
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


def filter_provided(proposals, persons):
    nproposals = []
    for proposal in proposals:
        found = False
        for componist in persons:
            if proposal['FirstName'] == componist['FirstName'] and proposal['LastName'] == componist['LastName']:
                found = True
        if not found:
            nproposals.append(proposal)
    return nproposals


def get_proposals(cuesheets, album, album_componisten):
    componisten = get_componisten()
    aliasses = get_componist_aliasses()
    proposals = []
    for cuesheet in cuesheets:
        proposals = proposals + has_person(cuesheet['Title'], componisten)
        proposals = proposals + has_person(cuesheet['Filename'], componisten)
        proposals = proposals + has_alias(cuesheet['Title'], aliasses, 'ComponistID')
        proposals = proposals + has_alias(cuesheet['Filename'], aliasses, 'ComponistID')
    proposals = proposals + has_person(album['Title'], componisten)
    proposals = proposals + has_alias(album['Title'], aliasses, 'ComponistID')
    proposals = ontdubbel(proposals)
    proposals = filter_provided(proposals, album_componisten)
    return proposals


def get_artists(cuesheets, album, album_performers):
    performers = get_performers()
    aliasses = get_performer_aliasses()
    proposals = []
    for cuesheet in cuesheets:
        proposals = proposals + has_person(cuesheet['Title'], performers)
        proposals = proposals + has_person(cuesheet['Filename'], performers)
        proposals = proposals + has_person(cuesheet['cue'].get('performer'), performers)
        proposals = proposals + has_alias(cuesheet['Title'], aliasses, 'PerformerID')
        proposals = proposals + has_alias(cuesheet['Filename'], aliasses, 'PerformerID')
    proposals = proposals + has_person(album['Title'], performers)
    proposals = ontdubbel(proposals)
    proposals = filter_provided(proposals, album_performers)
    return proposals


def organize_pieces(album_id, album_path):
    items = get_pieces(album_id)
    cuesheets = []
    pieces = []
    notfounds = []
    for item in items:
        ffile = item[0]
        if ffile:
            path = u'{}/{}'.format(album_path, ffile)
            if os.path.exists(path):
                extension = ffile.split('.')[-1]
                if extension == 'cue':
                    cuesheets.append(get_full_cuesheet(path, item[1]))
                else:
                    pieces.append(item)
            else:
                notfounds.append(path)
    return cuesheets, pieces, notfounds


def album_next(request, album_id):
    template = loader.get_template('flac/album.html')
    album_o = get_album(album_id)
    if album_o['AlbumID']:
        next_id = get_next_album(album_o['AlbumID'], album_id)
        if next_id:
            album_id = next_id
            print('next id: {}'.format(next_id))
    context = album_context(album_id)
    return HttpResponse(template.render(context, request))


def album_prev(request, album_id):
    template = loader.get_template('flac/album.html')
    album_o = get_album(album_id)
    if album_o['AlbumID']:
        prev_id = get_prev_album(album_o['AlbumID'], album_id)
        if prev_id:
            album_id = prev_id
            print('prev id: {}'.format(prev_id))
    context = album_context(album_id)
    return HttpResponse(template.render(context, request))


def album_context(album_id):
    album_o = get_album(album_id)
    if not album_o:
        return None

    mother_title = None
    proposals, artists = [], []
    album_o = get_album(album_id)
    if album_o['AlbumID']:
        mother_title = get_mother_title(album_o['AlbumID'])
    cuesheets, pieces, notfounds = organize_pieces(album_id, album_o['Path'])
    album_componisten = get_album_componisten(album_id)
    album_performers = get_album_performers(album_id)
    album_instruments = get_album_instruments(album_id)
    sp = get_setting('show_proposals')
    show_proposals = sp['VALUE']
    if show_proposals == '1':
        proposals = get_proposals(cuesheets, album_o, album_componisten)
        artists = get_artists(cuesheets, album_o, album_performers)
    return {
        'albumid': album_id,
        'pieces': pieces,
        'albums': get_album_albums(album_id),
        'album': album_o,
        'mother_title': mother_title,
        'album_componisten': album_componisten,
        'album_performers': album_performers,
        'album_instrument': album_instruments,
        'cuesheets': cuesheets,
        'notfounds': notfounds,
        'album_tags': get_album_tags(album_id),
        'proposals': proposals,
        'show_proposals': show_proposals,
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
