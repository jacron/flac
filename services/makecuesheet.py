import os

from . import trimextension, filename
from ..db import connect, get_album_path_by_id, insert_piece, get_piece


def write_cuesheet(name, album_id, content):
    conn, cursor = connect()
    cuename = u'{}.cue'.format(name)
    path = get_album_path_by_id(album_id, cursor)
    wpath = u'{}/{}'.format(path, cuename)
    f = open(wpath, 'w')
    f.write(content)
    f.close()
    insert_piece(
        name=cuename,
        code=0,
        album_id=album_id,
        c=cursor,
        conn=conn)


def rename_cuesheet(piece_id, album_id):
    print(piece_id, album_id)
    conn, cursor = connect()
    path = get_album_path_by_id(album_id, cursor)
    piece = get_piece(piece_id)
    src = u'{}/{}'.format(path, piece['Name'])
    if os.path.exists(src):
        # change extension from 'cue' to 'cuex'
        trg = u'{}x'.format(src)
        if not os.path.exists(trg):
            os.rename(src, trg)
            print('renamed to:{}'.format(trg))
            return 'cuesheet extension renamed'
        return 'renamed file already exists'
    return 'file not found'


def make_cuesheet(name, ids, album_id):
    lines = ['TITLE "{}"'.format(name)]
    titles = []
    for piece_id in ids:
        piece = get_piece(piece_id)
        fpath = piece.get('Name')
        title = trimextension(filename(fpath))
        titles.append(title)
        lines.append('FILE "{}" WAVE'.format(fpath))
        lines.append('  TRACK 01 AUDIO')
        lines.append('    TITLE "{}"'.format(title))
        lines.append('    INDEX 01 00:00:00')
    content = ''
    for line in lines:
        content += line + '\n'
    write_cuesheet(name, album_id, content)
    # common = get_common(titles)
    # pass
    # print(get_common(titles))
    # print(titles)
