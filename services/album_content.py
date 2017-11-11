import os
from unidecode import unidecode

from ..db import (
    get_album, get_pieces, get_componisten, get_performers,
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
        if len(p) > 2 and person.get(id_field) and p in s:
            if id_field == 'ComponistID':
                fperson = get_componist(person.get(id_field))
            else:
                fperson = get_performer(person.get(id_field))
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
        for person in persons:
            if proposal['FirstName'] == person['FirstName'] and proposal['LastName'] == person['LastName']:
                found = True
        if not found:
            nproposals.append(proposal)
    return nproposals


def get_proposals_from_piece(piece, persons, aliasses, fieldname):
    proposals = []
    proposals += has_person(piece[0], persons)
    proposals += has_alias(piece[0], aliasses, fieldname)
    return proposals


def get_proposals_from_cuesheet(cuesheet, persons, aliasses, fieldname):
    proposals = []
    proposals += has_person(cuesheet['Title'], persons)
    proposals += has_person(cuesheet['Filename'], persons)
    proposals += has_person(cuesheet['cue'].get('performer'), persons)
    proposals += has_alias(cuesheet['cue'].get('performer'), aliasses, fieldname)
    proposals += has_alias(cuesheet['Title'], aliasses, fieldname)
    proposals += has_alias(cuesheet['Filename'], aliasses, fieldname)
    for file in cuesheet['cue']['files']:
        if file:
            for track in file['tracks']:
                if track:
                    proposals += has_alias(track['title'], aliasses, fieldname)
                    proposals += has_person(track['title'], persons)
    return proposals


def get_other_proposals(album, persons, aliasses, fieldname, album_persons):
    proposals = []
    proposals += has_person(album['Title'], persons)
    proposals += has_alias(album['Title'], aliasses, fieldname)
    return proposals


def filter_proposals(proposals, album_persons):
    proposals = ontdubbel(proposals)
    proposals = filter_provided(proposals, album_persons)
    return proposals


def get_proposals(cuesheets, pieces, album, album_componisten):
    componisten = get_componisten()
    aliasses = get_componist_aliasses()
    proposals = []
    for cuesheet in cuesheets:
        proposals += get_proposals_from_cuesheet(cuesheet, componisten, aliasses, 'ComponistID')
    for piece in pieces:
        proposals += get_proposals_from_piece(piece, componisten, aliasses, 'ComponistID')
    proposals += get_other_proposals(album, componisten, aliasses, 'ComponistID', album_componisten)
    proposals = filter_proposals(proposals, album_componisten)
    return proposals


def get_artists(cuesheets, pieces, album, album_performers):
    performers = get_performers()
    aliasses = get_performer_aliasses()
    proposals = []
    for cuesheet in cuesheets:
        proposals += get_proposals_from_cuesheet(cuesheet, performers, aliasses, 'PerformerID')
    proposals += get_other_proposals(album, performers, aliasses, 'ComponistID', album_performers)
    proposals = filter_proposals(proposals, album_performers)
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
        proposals = get_proposals(cuesheets, pieces, album_o, album_componisten)
        artists = get_artists(cuesheets, pieces, album_o, album_performers)
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
