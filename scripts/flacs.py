"""flac

"""
import glob
import sqlite3
# importing for stand alone script
from venv.flac.db import (insert_album, insert_componist, insert_performer, insert_instrument, insert_piece)

cuesheet_extension = '.cue'
flac_wild = "/*.flac"
# cue_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/sonaten piano/Sonatas - John Browning - piano"
# cue_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/sonaten piano/Sonatas - Horowitz - piano"
cue_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/sonaten piano/sonatas scarlatti - schiff"

flac_path = cue_path + flac_wild
k_split = " K."
artiest = "Andres Schiff"
instrument = "Piano"
rows = []
# combine_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/sonaten clavecimbel/Sonatas - Belder/"
# combine_part = ["Disc 1of3", "Disc 2of3", "Disc 3of3", ]


def script_connect():
    # let op: het pad naar de database moet relatief zijn, omdat dit script stand alone uitgevoerd wordt!
    conn = sqlite3.connect('../../db.sqlite3')
    c = conn.cursor()
    return conn, c


def process_file(filepath):
    w = filepath.split('/')
    ffilename = w[-1]
    nr = ffilename.split()[0]
    print(ffilename)
    k = ffilename.split(k_split)[1]
    knr = k.split()[0]
    rows.append({
        "knr": knr,
        "link_name": artiest + " " + nr,
        "link_href": "file://" + filepath,
    })


def store_pieces():
    conn, c = script_connect()
    w = cue_path.split('/')
    album_title = w[-1]
    componist = w[-3]

    performer_id = insert_performer(artiest, c, conn)
    componist_id = insert_componist(componist, c, conn)
    instrument_id = insert_instrument(instrument, c, conn)
    album_id = insert_album(
        title=album_title,
        path=cue_path,
        instrument_id=instrument_id[0],
        performer_id=performer_id[0],
        componist_id=componist_id[0],
        c=c,
        conn=conn)
    print(flac_path)
    [process_file(f) for f in glob.iglob(flac_path)]
    for nr, row in enumerate(rows):
        insert_piece(row['link_href'], row['knr'], album_id[0], c, conn)
    conn.close()


def main():
    store_pieces()


if __name__ == '__main__':
    main()
