from __future__ import unicode_literals
# encoding: utf-8
# coding=utf-8
import glob

from flac.lib.color import ColorPrint
from flac.services import get_full_cuesheet
from flac.views import openfinder_album

"""flac

"""
import os
import sqlite3
from venv.flac.db import (
    insert_album, insert_instrument, get_album_count_by_path, get_album_by_path,
    set_album_title, get_componist_path_c, get_album_path_by_id,
)
from venv.flac.scripts.helper.rename import (
    rename_cover, restore_cover, sanatize_haakjes, rename_to_back, rename_all_titles,
)
from venv.flac.scripts.helper.insert import (
    insert_artiest, insert_composer, insert_componist_by_id, insert_performer_by_id,
    insert_pieces,
)


db_path = '../../db.sqlite3'
skipdirs = ['website', 'artwork', 'Artwork', 'etc', 'scans', 'Scans', 'scan',
            'website boxset', '#Booklets', 'Pixels', 'Graphics', 'Info + Art', 'Art', ]
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


def get_album_groups(path, mother_id, iscollectie, step_in):
    '''
    Behandel het path als plaats waar de subdirectories groepen albums bevatten
    '''
    for d in os.listdir(path):
        p = u'{}/{}'.format(path, d)
        if os.path.isdir(p) and d not in skipdirs:
            process_a(p, mother_id, iscollectie, step_in)


def get_albums(path, mother_id, iscollectie):
    '''
    Behandel het path als plaats waar de albums staan
    '''
    for d in os.listdir(path):
        p = u'{}/{}'.format(path, d)
        if os.path.isdir(p) and d not in skipdirs:
            process_album(p, mother_id, iscollectie)


def rename_titles(path):
    conn, c = script_connect()
    rename_all_titles(path, skipdirs, c, conn)


def get_path_of_componist(componist_id):
    if componist_id is None:
        print('No componist ID given, so quitting')
        return
    conn, c = script_connect()
    return get_componist_path_c(componist_id, c)


def get_path_of_album(album_id):
    if album_id is None:
        print('No album ID given, so quitting')
        return
    conn, c = script_connect()
    return get_album_path_by_id(album_id, c)


def get_path_by_albumid(album_id):
    conn, c = script_connect()
    return get_album_path_by_id(album_id, c)


def open_finder_album(album_id):
    path = get_path_by_albumid(album_id)
    os.system('open "{}"'.format(path))


def from_path(path):
    if path is None:
        raise Exception('No path given')
    w = path.split('/')
    return w[-1]


def main():
    global artiest, instrument, componist, ComponistID, PerformerID
    # process_pieces(path, album_id=)
    # ComponistID = 1
    # componist = ""
    # open_finder_album(album_id=)
    # return
    # path = get_path_of_componist(ComponistID)
    album_id = 191
    path = get_path_of_album(album_id)
    # path = "/Volumes/Media/Audio/Klassiek/Componisten/Hamza El Din"
    # path = "/Volumes/Media/Audio/Klassiek/Componisten/Sallinen"
    # componist = from_path(path)
    ColorPrint.print_c(path, ColorPrint.LIGHTCYAN)
    if path is None:
        print('No path')
        return
    # sanatize_haakjes(path, True)
    restore_cover(path=path, step_in=True)
    # rename_cover(path=path, step_in=True)
    # rename_titles(path)
    # rename_to_back(path)
    # process_a(p=path, mother_id=album_id, iscollectie=0, step_in=True)
    # get_albums(path=path, mother_id=None, iscollectie=0)
    # get_album_groups(path=path, mother_id=None, iscollectie=0, step_in=True)
    # album_id = process_album(path=path, mother_id=None, is_collectie=0)

if __name__ == '__main__':
    main()
