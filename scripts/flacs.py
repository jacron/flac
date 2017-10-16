# coding=utf-8
"""flac

"""
import os
import glob
import sqlite3

from flac import settings


# importing for stand alone script
from venv.flac.db import (
    insert_album, insert_componist, insert_performer, insert_instrument,
    insert_piece, insert_album_performer, insert_album_componist, get_album_by_title, )

play_types = ('cue', "flac", "ape", "mp3", "iso", "wma", "wav", "mp3", "m4a", )

k_split = None
artiest = None
componist = 'Bach, JS'
instrument = 'Cello'
rows = []


def script_connect():
    # let op: het pad naar de database moet hier relatief zijn, omdat dit script stand alone uitgevoerd wordt!
    conn = sqlite3.connect('../../db.sqlite3')
    c = conn.cursor()
    return conn, c


def process_file(filepath):
    print(filepath)
    w = filepath.split('/')
    ffilename = w[-1]
    print(ffilename)
    knr = 0
    if k_split:
        k = ffilename.split(k_split)[1]
        knr = k.split()[0]
    ffilename = filepath.split('/')[-1]
    ffilename = ffilename.replace("_", " ")
    rows.append({
        "knr": knr,
        "name": ffilename
    })


def insert_pieces(path, album_id, conn, c):
    global rows
    # print(path)
    for card in play_types:
        files_path = u"{}{}".format(path, "/*.{}".format(card))
        [process_file(f) for f in glob.iglob(files_path)]
    for row in rows:
        insert_piece(
            name=row['name'],
            code=row['knr'],
            album_id=album_id,
            c=c,
            conn=conn)


def insert_artiest(artiest, c, conn, album_id):
    if artiest:
        performer_id = insert_performer(artiest, c, conn)[0]
    else:
        performer_id = None
    if performer_id:
        insert_album_performer(performer_id, album_id, c, conn)


def insert_composer(componist, c, conn, album_id):
    if componist:
        componist_id = insert_componist(componist, c, conn)[0]
    else:
        componist_id = None
    if componist_id:
        insert_album_componist(componist_id, album_id, c, conn)


def process_album(path, mother_id, is_collectie):
    global rows
    rows = []

    if len(path.split('[')) > 1:
        print('cue_path mag geen vierkante haken ([]) bevatten! - quitting')
        return
    conn, c = script_connect()
    w = path.split('/')
    album_title = w[-1].replace("_", "")

    if instrument:
        instrument_id = insert_instrument(instrument, c, conn)[0]
    else:
        instrument_id = None
    album_id = insert_album(
        title=album_title,
        path=path.decode('latin-1').encode('utf-8'),
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


def rename_frontjpg(path, name):
    src = '{}/{}.jpg'.format(path, name)
    trg = '{}/{}'.format(path, 'folder.jpg')
    if os.path.exists(trg):
        return

    if os.path.exists(src):
        os.rename(src, trg)
        print('renamed to:{}'.format(trg))
    else:
        wild = '{}/front*.jpg'.format(path)
        pics = glob.glob(wild)
        if len(pics) > 0:
            src = pics[0]
            print('renaming {}\n to:{}'.format(src, trg))
            os.rename(src, trg)
        else:
            wild = '{}/*.jpg'.format(path)
            pics = glob.glob(wild)
            if len(pics) > 0:
                src = pics[0]
                print('renaming {}\n to:{}'.format(src, trg))
                os.rename(src, trg)


def process_path(path, f):
    print(f)
    p = '{}/{}'.format(path, f)
    if os.path.isdir(p):
        for ff in os.listdir(p):
            print(ff)
            src = u'{}/{}'.format(p, ff)
            trg = u'{}/{}'.format(os.path.dirname(p), ff)
            print(src)
            print(trg)
            print('--')
            # os.rename(p, trg)


def replace_haakjes(s):
    for ch in ['[', '{']:
        if ch in s:
            s = s.replace(ch, '(')
    for ch in [']', '}']:
        if ch in s:
            s = s.replace(ch, ')')
    return s


def has_haakjes(s):
    for ch in ['[', '{']:
        if ch in s:
            return True
    for ch in [']', '}']:
        if ch in s:
            return True
    return False


def process_dir(path, mother_id, iscollectie):
    for d in os.listdir(path):
        p = '{}/{}'.format(path, d).decode('latin-1').encode('utf-8')
        if os.path.isdir(p) and d != 'website' and d != 'artwork' and d != 'Artwork' and d != 'etc' and d != 'scans':
            # rename_frontjpg(p, 'box front')
            # print(p, mid, iscollectie)
            # process_album(p, mid, iscollectie)
            w = p.split('/')
            album_title = w[-1].replace("_", "")
            conn, c = script_connect()
            found = get_album_by_title(album_title, c, conn)
            # print album_title

            if found['Count'] == 0:
                # print album_title
                process_album(p, mother_id, iscollectie)
                # print replace_haakjes(album_title)
                # if has_haakjes(album_title):
                #     src = '{}/{}'.format(path, album_title)
                #     dst = '{}/{}'.format(path, replace_haakjes(album_title))
                #     # print(src)
                #     # print(dst)
                #     if os.path.exists(src):
                #         os.rename(src, dst)
                #     else:
                #         print(src)


def main():
    paths = []
    ids = []
    # paths.append("/Volumes/Media/Audio/Klassiek/Collecties/BBC Legends")
    # ids.append(168)
    # rename_frontjpg(path)
    # print(path)

    # for path, mid in zip(paths, ids):
    # nr = 24
    # path = paths[nr]
    # mid = ids[nr]
    # print(path, mid)
    # mid = 169
    mid = None
    # path="/Volumes/Media/Audio/Klassiek/Collecties/BBC Legends/BBCL4015 - Gilels - Schumane, Scarlatti, Bach"
    # path="/Volumes/Media/Audio/Klassiek/Collecties/Classic Voice Antiqua/ClassicAntiqua_15-WAV"
    path="/Volumes/Media/Audio/Klassiek/Verzamelalbums"
    # path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/Christopher Page, Gothic Voices - The earliest songbook in England"
    # path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/Christopher Page, Gothic Voices - The Spirits of England and France - vol 3"
    # path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/Grieg - Sibelius"
    # path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/historisch russisch archief"
    # path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/Jefta"
    # path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/Ferrara Ensemble - Figures of Harmony - Songs of Codex Chantilly C. 1390 (2015) (FLAC)"
    # path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/Gale 96k_1976-77"
    # path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/High Def Vinyls 96K24B (Miller & Kreisel) Limited Edition Vol. 1, 3, 5 (24)"
    # path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/Jean Cocteau et Les Six"
    # path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/Komitas Armenian Liturgy"
    path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/Phase 4 Concert Series Complete - 2496"
    path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/RenaissanceMusic"
    path="/Volumes/Media/Audio/Klassiek/Verzamelalbums/Rossini - Respighi - Lamberto Gardelli (24)"
    path="/Volumes/Media/Audio/Klassiek/Componisten/Bach/Cello"
    path="/Volumes/Media/Audio/Klassiek/Componisten/Bach/Cello/Rostropovich"
    path="/Volumes/Media/Audio/Klassiek/Componisten/Bach/Cello/Heinrich Schiff"
    process_dir(path=path, mother_id=2167, iscollectie=0)
    # process_album(path=path, mother_id=None, is_collectie=2)


if __name__ == '__main__':
    main()
