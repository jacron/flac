# encoding: utf-8
# coding=utf-8
"""flac

"""
import os
import unicodedata
import sqlite3
from venv.flac.db import (
    insert_album, insert_instrument, get_album_by_path, )
from venv.flac.scripts.helper.rename import (
    rename_cover, sanatize_haakjes
)
from venv.flac.scripts.helper.insert import (
    insert_artiest, insert_composer, insert_pieces
)

db_path = '../../db.sqlite3'
skipdirs = ['website', 'artwork', 'Artwork', 'etc', 'scans',
            'website boxset', '#Booklets', 'Pixels']
artiest = None
componist = None
instrument = None


def script_connect():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    return conn, c


def process_pieces(path, album_id):
    conn, c = script_connect()
    insert_pieces(path, album_id, conn, c)


def process_album(path, mother_id, is_collectie):
    if len(path.split('[')) > 1:
        print('cue_path mag geen vierkante haken ([]) bevatten! - quitting')
        return
    conn, c = script_connect()
    w = path.split('/')
    album_title = w[-1].replace("_", " ")

    if instrument:
        instrument_id = insert_instrument(instrument, c, conn)[0]
    else:
        instrument_id = None
    album_id = insert_album(
        title=album_title,
        path=path,  # .decode('latin-1').encode('utf-8'),
        instrument_id=instrument_id,
        is_collectie=is_collectie,
        c=c,
        conn=conn,
        album_id=mother_id,
    )[0]
    print("album_id={}".format(album_id))
    insert_pieces(path, album_id, conn, c)
    insert_artiest(artiest, c, conn, album_id)
    insert_composer(componist, c, conn, album_id)
    conn.close()
    return album_id


def count_album_by_path(p):
    conn, c = script_connect()
    found = get_album_by_path(p, c, conn)
    return found['Count']


def process_a(p, mother_id, iscollectie, step_in):
    album_id = process_album(p, mother_id, iscollectie)
    if step_in:
        # one recursive step
        for d2 in os.listdir(p):
            p2 = u'{}/{}'.format(p, d2)  # .decode('latin-1').encode('utf-8')
            if os.path.isdir(p2) and d2 not in skipdirs:
                process_album(p2, album_id, 0)


def process_p(path, p, d, mother_id, iscollectie, cmd, step_in):
    print(cmd)
    if cmd == 'sanatize':
        sanatize_haakjes(path, d)
    if cmd == 'cover':
        rename_cover(p)
    if cmd == 'process':
        # if count_album_by_path(p) == 0:
        process_a(p, mother_id, iscollectie, step_in)


def process_dir(path, mother_id, iscollectie, cmd, step_in):
    for d in os.listdir(path):
        p = u'{}/{}'.format(path, d)  # .decode('latin-1').encode('utf-8')
        if os.path.isdir(p) and d not in skipdirs:
            process_p(path, p, d, mother_id, iscollectie, cmd, step_in)


def main():
    global artiest, instrument, componist
    componist = "JS Bach"
    # componist = "Heinrich Albert"
    # instrument = "Clavecimbel"
    # cmd = 'sanatize'
    # cmd = 'cover'
    cmd = 'process'

    # path="/Volumes/Media/Audio/Klassiek/Componisten/Mahler/Symfonie 10"
    # path="/Volumes/Media/Audio/Klassiek/Componisten/Mahler/Amsterdam Mahlerfeest 1995"
    # path="/Volumes/Media/Audio/Klassiek/Componisten/Mahler/Amsterdam Mahlerfeest 1995/cd 11"
    path = u"/Volumes/Media/Audio/Klassiek/Componisten/Bach/Rilling - Bach Complete Edition - Hanssler"
    path = u"/Volumes/Media/Audio/Klassiek/Componisten/Albert"
    path = "/Volumes/Media/Audio/Klassiek/Componisten/Bach/Rilling - Sacred Works (11 cds)"
    # process_pieces(path, album_id=666)
    # process_dir(path=path, iscollectie=0, cmd=cmd, mother_id=2198, step_in=True) # Rilling
    process_dir(path=path, iscollectie=0, cmd=cmd, mother_id=2196, step_in=False)
    # process_album(path=path, mother_id=2395, is_collectie=0)


if __name__ == '__main__':
    main()
