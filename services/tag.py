import taglib
import os

from flac.db import get_album, get_pieces
from flac.services import get_extension


def title2tag(album, name):
    song = taglib.File(os.path.join(album['Path'], name))
    print song.length
    # song.tags['COMPOSER'] = composer
    # song.tags['ALBUM'] = [album['Title']]
    # song.save()


def title_tag(album_id):
    album = get_album(album_id)
    print(album['Title'])
    pieces = get_pieces(album_id)
    for piece in pieces:
        if get_extension(piece['Name']) <> 'cue':
            # print piece['Name']
            title2tag(album, piece['Name'])

    return ''
