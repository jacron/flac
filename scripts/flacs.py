from __future__ import unicode_literals
# encoding: utf-8
# coding=utf-8
# import glob
from flac.db.pieces import insert_pieces
from flac.lib.color import ColorPrint
from flac.services import get_full_cuesheet
from flac.views import get_componist_path

"""flac

"""
import os
import sqlite3
from venv.flac.db import (
    insert_album, insert_instrument, get_album_count_by_path, get_album_by_path,
    set_album_title, get_componist_path_c, get_album_path_by_id,
    insert_componist, get_componist_path_by_id, get_componist_id_from_album)
from venv.flac.scripts.helper.rename import (
    rename_cover, restore_cover, sanatize_haakjes, rename_to_back, rename_all_titles,
)
from venv.flac.scripts.helper.insert import (
    insert_artiest, insert_composer, insert_componist_by_id, insert_performer_by_id,
)


db_path = '../../db.sqlite3'
skipdirs = ['website', 'artwork', 'Artwork', 'etc', 'scans', 'Scans', 'scan',
            'website boxset', '#Booklets', 'Pixels', 'Graphics', 'Info + Art', 'Art',
            'Covers', ]
artiest = None
componist = None
ComponistID = None
PerformerID = None
PerformerID2 = None
instrument = None


def script_connect():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    return conn, c


def process_pieces(path, album_id):
    conn, c = script_connect()
    insert_pieces(path, album_id, conn, c)


def process_album(path, mother_id, is_collectie):
    """
    haal stukken (cuesheets en music files) op voor een album
    """
    global componist, ComponistID, PerformerID, artiest
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
    insert_pieces(path, album_id, conn, c)
    if PerformerID:
        insert_performer_by_id(PerformerID, c, conn, album_id)
    else:
        if artiest:
            insert_artiest(artiest, c, conn, album_id)
    if PerformerID2:
        insert_performer_by_id(PerformerID2, c, conn, album_id)
    if ComponistID:
        insert_componist_by_id(ComponistID, c, conn, album_id)
    else:
        if componist:
            insert_composer(componist)
    conn.close()
    return album_id


def count_album_by_path(p):
    conn, c = script_connect()
    found = get_album_count_by_path(p, c, conn)
    return found['Count']


def process_a(p, mother_id, iscollectie, step_in):
    '''
    Lees in directory p alle stukken in voor een album, onthoud album_id als mother. Als step_in waar is, doe hetzelfde in de subdirectories (1 niveau diep) met album_id als mother.
    '''
    album_id = process_album(p, mother_id, iscollectie)
    if step_in:
        # one recursive step
        for d2 in os.listdir(p):
            p2 = u'{}/{}'.format(p, d2)
            if os.path.isdir(p2) and d2 not in skipdirs:
                album_id2 = process_album(p2, album_id, 0)
                if step_in == 2:
                    # second recurisve step
                    for d3 in os.listdir(p2):
                        p3 = u'{}/{}'.format(p, d3)
                        if os.path.isdir(p3) and d3 not in skipdirs:
                            process_album(p3, album_id2, 0)


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


def get_path_by_componistid(album_id):
    conn, c = script_connect()
    return get_componist_path_by_id(album_id, c)


def open_finder_album(album_id):
    path = get_path_by_albumid(album_id)
    os.system('open "{}"'.format(path))


def open_finder_componist(componist_id):
    path = get_path_by_componistid(componist_id)
    os.system('open "{}"'.format(path))


def from_path(path):
    if path is None:
        raise Exception('No path given')
    w = path.split('/')
    return w[-1]


def insert_composer(name):
    conn, c = script_connect()
    return insert_componist(name, c, conn)


def componist_from_album(album_id):
    conn, c = script_connect()
    cid = get_componist_id_from_album(album_id, c)
    return cid


def main():
    global artiest, instrument, componist, ComponistID, PerformerID, PerformerID2

    path = ""
    # ComponistID = insert_composer('Zinnstag')[0]
    # print(ComponistID)
    # return

    # open_finder_album(album_id=)
    # open_finder_componist(ComponistID)
    # return
    # path = get_path_of_componist(ComponistID)
    # album_id = 169
    # path = get_path_of_album(album_id)
    # mother_id = 3816
    # path = "/Volumes/Media/Audio/Klassiek/Collecties/Yo Yo Ma 30 years outside the box"
    path = "/Volumes/Media/Audio/Klassiek/Collecties/Decca, The Decca Sound"
    # artiest = "Fritz Reiner"
    # ComponistID = 134
    # componist = from_path(path)
    # ComponistID = componist_from_album(album_id)
    # PerformerID = 112
    # PerformerID2 = 47
    ColorPrint.print_c(path, ColorPrint.LIGHTCYAN)
    if path is None:
        print('No path')
        return
    # process_pieces(path, album_id=album_id)
    # return

    # sanatize_haakjes(path, True)
    # restore_cover(path=path, step_in=True)
    # rename_cover(path=path, step_in=True)
    # rename_titles(path)
    rename_to_back(path)
    # process_a(p=path, mother_id=None, iscollectie=1, step_in=1)
    # get_albums(path=path, mother_id=None, iscollectie=1)
    # get_album_groups(path=path, mother_id=None, iscollectie=0, step_in=True)
    # album_id = process_album(path=path, mother_id=None, is_collectie=0)

if __name__ == '__main__':
    main()
