import taglib
import os

from flac.db import get_album, get_pieces, get_album_performers, \
    get_album_componisten
from flac.services import get_extension


def performers(album_id):
    p = get_album_performers(album_id)
    return [x['FullName'] for x in p]


def composers(album_id):
    p = get_album_componisten(album_id)
    return [x['FullName'] for x in p]


def title2tag(p, title):
    song = taglib.File(p)
    song.tags['ALBUM'] = [title]
    song.save()


def all2tag(p, title, album_id):
    song = taglib.File(p)
    song.tags['ALBUM'] = [title]
    song.tags['ARTIST'] = performers(album_id)
    song.tags['COMPOSER'] = composers(album_id)
    song.save()


def set_metatags(album_id, mode):
    album = get_album(album_id)
    print(album['Title'])
    pieces = get_pieces(album_id)
    for piece in pieces:
        if get_extension(piece['Name']) <> 'cue':
            p = os.path.join(album['Path'], piece['Name'])
            if mode == 'short':
                title2tag(p, album['Title'])
            if mode == 'long':
                all2tag(p, album['Title'], album['ID'])
    return ''


def get_metatags(path):
    song = taglib.File(path)
    return song.tags
