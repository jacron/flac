import codecs
import glob
import os

from flac.scripts import play_types, kirkpatrick
from . import trimextension, filename
from ..db import connect, get_album_path_by_id, insert_piece, get_piece


def write_cuesheet(name, album_id, lines):
    content = ''
    for line in lines:
        content += line + '\n'
    conn, cursor = connect()
    cuename = u'{}.cue'.format(name)
    path = get_album_path_by_id(album_id, cursor)
    wpath = u'{}/{}'.format(path, cuename)
    # https://stackoverflow.com/questions/934160/write-to-utf-8-file-in-python
    with codecs.open(wpath, 'w', 'utf-8') as f:
        f.write(u'\ufeff')
        f.write(u'{}'.format(content))
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
    lines = []
    lines.append(u'TITLE "{}"'.format(filename(name)))
    # titles = []
    for piece_id in ids:
        piece = get_piece(piece_id)
        fpath = piece.get('Name')
        title = trimextension(filename(fpath))
        # titles.append(title)
        lines.append(u'FILE "{}" WAVE'.format(fpath))
        lines.append(u'  TRACK 01 AUDIO')
        lines.append(u'    TITLE "{}"'.format(title))
        lines.append(u'    INDEX 01 00:00:00')
    write_cuesheet(name, album_id, lines)


def get_dirs(path):
    dirs = []
    for d in os.listdir(path):
        if os.path.isdir(os.path.join(path, d)):
            dirs.append(d)
    return dirs


# def insert_sub_pieces(path, album_id, conn, c):
#     ids = []
#     for card in play_types:
#         files_path = u"{}{}".format(path, "/*.{}".format(card))
#         for f in glob.iglob(files_path):
#             print(f)
#             fname = os.path.join(f.split('/')[-2:])  # include subdir in fname
#             id = insert_piece(
#                 name=fname,
#                 code=kirkpatrick(f),
#                 album_id=album_id,
#                 c=c,
#                 conn=conn)
#             ids.append(id)
#     return ids


def make_sub_cuesheet(path, album_id):
    cue_title = filename(path)
    lines = []
    for card in play_types:
        files_path = u"{}{}".format(path, "/*.{}".format(card))
        for f in glob.iglob(files_path):
            print(f)
            fname = os.path.join(f.split('/')[-2:])  # include subdir in fname
            title = trimextension(filename(f))
            lines.append(u'TITLE "{}"'.format(title))
            lines.append(u'FILE "{}" WAVE'.format(f))
            lines.append(u'  TRACK 01 AUDIO')
            lines.append(u'    TITLE "{}"'.format(title))
            lines.append(u'    INDEX 01 00:00:00')
    write_cuesheet(cue_title, album_id, lines)


def make_subs_cuesheet(album_id):
    conn, c = connect()
    path = get_album_path_by_id(album_id, c)
    dirs = get_dirs(path)
    for d in dirs:
        p = os.path.join(path, d)
        make_sub_cuesheet(p, album_id)
