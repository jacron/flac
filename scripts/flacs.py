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

play_types = ('cue', "flac", "ape", "mp3", "iso", "wma")

k_split = None
# artiest="Wilhelm Kempf"
artiest=None
# componist = "Gustav Mahler"
# componist="Beethoven, Ludwig von"
componist = None
# instrument = "Piano"
instrument = None
# mother_album_id = 50 # beethoven piano solo
# mother_album_id = 72 # ronald brautigam
# mother_album_id = 85 # wilhelm kempf
# mother_album_id = 94 # archiv produktion
mother_album_id=150  # avant garde
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
        print(files_path)
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


def process_album(path):
    global rows
    rows = []

    if len(path.split('[')) > 1:
        print('cue_path mag geen vierkante haken ([]) bevatten! - quitting')
        return
    conn, c = script_connect()
    w = path.split('/')
    album_title = w[-1].replace("_", "")

    if artiest:
        performer_id = insert_performer(artiest, c, conn)[0]
    else:
        performer_id = None
    if componist:
        componist_id = insert_componist(componist, c, conn)[0]
    else:
        componist_id = None
    if instrument:
        instrument_id = insert_instrument(instrument, c, conn)[0]
    else:
        instrument_id = None
    album_id = insert_album(
        title=album_title,
        path=path,
        instrument_id=instrument_id,
        is_collectie=0,
        c=c,
        conn=conn,
        album_id=mother_album_id,
    )[0]
    print("album_id={}".format(album_id))
    insert_pieces(path, album_id, conn, c)
    if performer_id:
        insert_album_performer(performer_id, album_id, c, conn)
    if componist_id:
        insert_album_componist(componist_id, album_id, c, conn)
    conn.close()


def rename_frontjpg(path):
    src = '{}/{}'.format(path, 'front.jpg')
    trg = '{}/{}'.format(path, 'folder.jpg')
    if os.path.exists(src):
        print('renamed to:{}'.format(trg))
        os.rename(src, trg)


def main():
    # for i in range(48, 56):  # 38):
    #     nr = i
    #     if i < 10:
    #         nr = '0{}'.format(i)
    #     path = '{}{}'.format(cue_path, nr)

    # path = "/Volumes/Media/Audio/Klassiek/Collecties/Archiv Produktion 1947 - 2013/archiv_produktion_1947_2013_40b"
    # path="/Volumes/Media/Audio/Klassiek/Collecties/Avant Garde Project"
    path="/Volumes/Media/Audio/Klassiek/Collecties/Avant Garde Project/AGP151 - Alban Berg"
    # rename_frontjpg(path)
    # print(path)
    process_album(path)


if __name__ == '__main__':
    main()
