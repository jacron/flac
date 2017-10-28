from __future__ import unicode_literals
# encoding: utf-8
# coding=utf-8
import glob

from flac.lib.color import ColorPrint
from flac.services import get_full_cuesheet

"""flac

"""
import os
import sqlite3
from venv.flac.db import (
    insert_album, insert_instrument, get_album_count_by_path, get_album_by_path,
    set_album_title,
)
from venv.flac.scripts.helper.rename import (
    rename_cover, restore_cover, sanatize_haakjes, rename_to_back,
)
from venv.flac.scripts.helper.insert import (
    insert_artiest, insert_composer, insert_componist_by_id, insert_performer_by_id,
    insert_pieces,
)


db_path = '../../db.sqlite3'
skipdirs = ['website', 'artwork', 'Artwork', 'etc', 'scans', 'Scans', 'scan',
            'website boxset', '#Booklets', 'Pixels', 'Graphics', ]
artiest = None
componist = None
ComponistID = None
PerformerID = None
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
        path=path,
        instrument_id=instrument_id,
        is_collectie=is_collectie,
        c=c,
        conn=conn,
        album_id=mother_id,
    )[0]
    ColorPrint.print_c("album_id={}".format(album_id), ColorPrint.LIGHTCYAN)
    # print("album_id={}".format(album_id))
    insert_pieces(path, album_id, conn, c)
    if PerformerID:
        insert_performer_by_id(PerformerID, c, conn, album_id)
    else:
        insert_artiest(artiest, c, conn, album_id)

    if ComponistID:
        insert_componist_by_id(ComponistID, c, conn, album_id)
    else:
        insert_composer(componist, c, conn, album_id)
    conn.close()
    return album_id


def count_album_by_path(p):
    conn, c = script_connect()
    found = get_album_count_by_path(p, c, conn)
    return found['Count']


def album_by_path(p):
    conn, c = script_connect()
    return get_album_by_path(p, c, conn)


def process_a(p, mother_id, iscollectie, step_in):
    '''
    Lees in directory p alle stukken in voor een album, onthoud album_id als mother.
    Als step_in waar is, doe hetzelfde in de subdirectories (1 niveau diep) met album_id als mother.
    '''
    album_id = process_album(p, mother_id, iscollectie)
    if step_in:
        # one recursive step
        for d2 in os.listdir(p):
            p2 = u'{}/{}'.format(p, d2)
            if os.path.isdir(p2) and d2 not in skipdirs:
                process_album(p2, album_id, 0)


def get_albums(path, mother_id, iscollectie, step_in):
    '''
    Behandel het path als plaats waar de subdirectories groepen albums bevatten
    '''
    for d in os.listdir(path):
        p = u'{}/{}'.format(path, d)
        if os.path.isdir(p) and d not in skipdirs:
            process_a(p, mother_id, iscollectie, step_in)


def rename_titles(path):
    conn, c = script_connect()
    for d in os.listdir(path):
        p = u'{}/{}'.format(path, d)
        if os.path.isdir(p) and d not in skipdirs:
            nr = u'{}{}'.format(d[-2],d[-1])
            # if int(nr) > 0:
            cuepath = u'{}/lijst.cue'.format(p)
            if not os.path.exists(cuepath):
                cuepath = u'{}/*.cue'.format(p)
                for ncue in glob.iglob(cuepath):
                    cuepath = ncue
                    # return
            cue = get_full_cuesheet(cuepath, 0)
            # full_title = '{} - {}'.format(nr, cue['Title'])
            full_title = '{}'.format(cue['Title'])
            print(full_title)

            album = album_by_path(p)
            print(album['Title'])
            set_album_title(album['ID'], full_title, c, conn)


def main():
    global artiest, instrument, componist, ComponistID, PerformerID
    # componist = "JS Bach"
    # instrument = "Clavecimbel"
    # PerformerID = 142 # Glenn Gould

    # process_pieces(path, album_id=666)
    # sanatize_haakjes(path, True)

    ComponistID = 45
    # path = "/Volumes/Media/Audio/Klassiek/Componisten/Boito"
    # path = "/Volumes/Media/Audio/Klassiek/Componisten/Bottesini"
    path = "/Volumes/Media/Audio/Klassiek/Componisten/Brahms"
    ColorPrint.print_c(path, ColorPrint.LIGHTCYAN)
    # rename_titles(path)
    # restore_cover(path, True)
    # rename_to_back(path)
    # process_a(p=path, mother_id=None, iscollectie=0, step_in=True)
    get_albums(path=path, mother_id=None, iscollectie=0, step_in=True)
    # album_id = process_album(path=path, mother_id=None, is_collectie=0)


if __name__ == '__main__':
    main()
