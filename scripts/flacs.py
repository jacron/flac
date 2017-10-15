# coding=utf-8
"""flac

"""
import os
import glob
import sqlite3
# importing for stand alone script
from venv.flac.db import (
    insert_album, insert_componist, insert_performer, insert_instrument,
    insert_piece, insert_album_performer, insert_album_componist, )

play_types = ('cue', "flac", "ape", "mp3", "iso", "wma", "wav", "mp3", )

k_split = None
artiest = None
componist = None
instrument = None
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
    print(path)
    for card in play_types:
        files_path = u"{}{}".format(path, "/*.{}".format(card))
        # print(files_path)
        [process_file(f) for f in glob.iglob(files_path)]
    # print(rows)
    for row in rows:
        # print(row['name'])
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
    # print (path)
    # print(mother_id)
    # return

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


def process_dir(path, mid):
    for d in os.listdir(path):
        p = '{}/{}'.format(path, d).decode('latin-1').encode('utf-8')
        if os.path.isdir(p) and d != 'website' and d != 'artwork':
            # rename_frontjpg(p, 'box front')
            process_album(p, mid, 0)


def main():
    paths = []
    ids = []
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/BBC Legends")
    ids.append(168)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Classic Voice Antiqua")
    ids.append(169)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Decca Legends")
    ids.append(170)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Decca Mono Years Complete - 2496")
    ids.append(171)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Decca, The Decca Sound")
    ids.append(172)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Deutsche Harmonia Mundi 50 Years")
    ids.append(173)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Deutsche Harmonia Mundi Collectie 50 CD")
    ids.append(174)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/DG - the originals")
    ids.append(175)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/DG - the originals - vinyl")
    ids.append(176)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/DG 111 years")
    ids.append(177)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/DG 111 YEARS B")
    ids.append(178)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Divox Antiqua Historic Organs Series")
    ids.append(179)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Franklin Mint")
    ids.append(180)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Harmonia Mundi - 50 years")
    ids.append(181)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Harmonia Mundi - Century Collection")
    ids.append(182)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Harmonia Mundi - Liturgie")
    ids.append(183)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Harmonia Mundi - Sacred Music")
    ids.append(184)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Mercury Living Presence")
    ids.append(185)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Mercury Living Presence 2")
    ids.append(186)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/MLP - box 2")
    ids.append(188)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Musik in Deutschland 1950-2000")
    ids.append(190)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Philips Duo")
    ids.append(191)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/RCA Living Stereo")
    ids.append(192)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Treasures of chamber music")
    ids.append(193)
    paths.append("/Volumes/Media/Audio/Klassiek/Collecties/Vivarte Sony 60 CD Collection")
    ids.append(168) # !!
    # rename_frontjpg(path)
    # print(path)

    # for path, mid in zip(paths, ids):
    # nr = 24
    # path = paths[nr]
    # mid = ids[nr]
    # print(path, mid)
    mid = 169
    path="/Volumes/Media/Audio/Klassiek/Collecties/BBC Legends/BBCL4015 - Gilels - Schumane, Scarlatti, Bach"
    PendingDeprecationWarning="/Volumes/Media/Audio/Klassiek/Collecties/Classic Voice Antiqua/ClassicAntiqua_15-WAV"
    # process_dir(path, mid)
    process_album(path, mid, 0)

if __name__ == '__main__':
    main()
