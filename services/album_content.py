# coding: utf-8
import os

from flac.services.proposals import get_proposals, get_artists
from flac.settings import SKIP_DIRS
from ..db import (
    get_album, get_pieces,
    get_mother_title, get_album_albums, get_album_componisten, get_album_performers, get_album_instruments,
    get_album_tags, get_setting, get_prev_album, get_next_album, get_prev_list_album,
    get_next_list_album)
from ..services import get_full_cuesheet


def has_notfound_files(cuesheet, album_path):
    # for file in cuesheet['cue']['files']:
        # fname = file['name'].encode('utf-8')
        # path = '{}/{}'.format(album_path, fname)
        # if not os.path.exists(path):
        #     return True
    # return False
    pass


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


def check_subdirs(path):
    for d in os.listdir(path):
        p = os.path.join(path, d)
        if os.path.isdir(p) and d not in SKIP_DIRS:
            return True
    return False


def album_context(album_id, list_name=None, list_id=None):
    album_o = get_album(album_id)
    if not album_o:
        return None
    mother_title, mother_id = None, None
    album_o = get_album(album_id)
    if album_o['AlbumID']:
        mother_id = album_o['AlbumID']
        mother_title = get_mother_title(mother_id)
    cuesheets, pieces, notfounds, invalidcues = organize_pieces(album_id, album_o['Path'])
    album_componisten = get_album_componisten(album_id)
    album_performers = get_album_performers(album_id)
    album_instruments = get_album_instruments(album_id)
    sp = get_setting('show_proposals')
    show_proposals = sp['VALUE']
    proposals, artists = [], []
    if show_proposals == '1':
        allsheets = cuesheets + invalidcues
        proposals = get_proposals(allsheets, pieces, album_o, album_componisten)
        artists = get_artists(allsheets, pieces, album_o, album_performers)
    next_list_id = get_next_list_album(album_id, list_name, list_id)
    prev_list_id = get_prev_list_album(album_id, list_name, list_id)
    if next_list_id:
        next_list_id = '{}/{}/{}/'.format(next_list_id, list_name, list_id)
    if prev_list_id:
        prev_list_id = '{}/{}/{}/'.format(prev_list_id, list_name, list_id)
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
        'prev_id': get_prev_album(mother_id, album_id),
        'next_id': get_next_album(mother_id, album_id),
        'prev_list_id': prev_list_id,
        'next_list_id': next_list_id,
        'has_subdirs': check_subdirs(album_o['Path']),
    }
