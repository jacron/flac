import os

from flac.services.proposals import get_proposals, get_artists
from ..db import (
    get_album, get_pieces,
    get_mother_title, get_album_albums, get_album_componisten, get_album_performers, get_album_instruments,
    get_album_tags, get_setting)
from ..services import get_full_cuesheet


def has_notfound_files(cuesheet, album_path):
    for file in cuesheet['cue']['files']:
        if not os.path.exists(u'{}/{}'.format(album_path, file['name'])):
            return True
    return False


def organize_pieces(album_id, album_path):
    items = get_pieces(album_id)
    cuesheets, pieces, notfounds, invalidcues = [], [], [], []
    for item in items:
        ffile = item[0]
        if ffile:
            path = u'{}/{}'.format(album_path, ffile)
            if os.path.exists(path):
                extension = ffile.split('.')[-1]
                if extension == 'cue':
                    cuesheet = get_full_cuesheet(path, item[1])
                    if has_notfound_files(cuesheet, album_path):
                        invalidcues.append(cuesheet)
                    else:
                        cuesheets.append(cuesheet)
                else:
                    pieces.append(item)
            else:
                notfounds.append(path)
    return cuesheets, pieces, notfounds, invalidcues


def album_context(album_id):
    album_o = get_album(album_id)
    if not album_o:
        return None

    mother_title = None
    proposals, artists = [], []
    album_o = get_album(album_id)
    if album_o['AlbumID']:
        mother_title = get_mother_title(album_o['AlbumID'])
    cuesheets, pieces, notfounds, invalidcues = organize_pieces(album_id, album_o['Path'])
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
        'invalidcues': invalidcues,
        'notfounds': notfounds,
        'album_tags': get_album_tags(album_id),
        'proposals': proposals,
        'show_proposals': show_proposals,
        'artists': artists,
    }
