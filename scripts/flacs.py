"""flac

"""
import glob
import sqlite3
# importing for stand alone script
from venv.flac.db import (insert_album, insert_componist, insert_performer, insert_instrument, insert_piece)

cuesheet_extension = '.cue'
cue_wild = '/*.cue'
flac_wild = "/*.flac"
# cue_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/sonaten piano/Sonatas - John Browning - piano"
# cue_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/sonaten piano/Sonatas - Horowitz - piano"
# cue_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/sonaten piano/sonatas scarlatti - schiff"
cue_path = '/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/sonaten piano/sonatas scarlatti - weissenberg'
# cue_path = '/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/Lettere Amorose - Il Complesso Barroco'
files_path = cue_path + cue_wild
# files_path = cue_path + flac_wild
k_split = None
# k_split = " K"
artiest = "Alexis Weissenberg"
# artiest = "John Browning"
# artiest = "Vladimir Horowitz"
# artiest = "Andres Schiff"
componist = "Scarlatti, D"
instrument = "Piano"
rows = []


def script_connect():
    # let op: het pad naar de database moet hier relatief zijn, omdat dit script stand alone uitgevoerd wordt!
    conn = sqlite3.connect('../../db.sqlite3')
    c = conn.cursor()
    return conn, c


def process_file(filepath):
    w = filepath.split('/')
    ffilename = w[-1]
    print(ffilename)
    knr = 0
    if k_split:
        k = ffilename.split(k_split)[1]
        knr = k.split()[0]
    filepath = ffilename.decode('utf-8')
    ffilename = filepath.split('/')[-1]
    rows.append({
        "knr": knr,
        "name": ffilename
    })


def store_pieces():
    conn, c = script_connect()
    w = cue_path.split('/')
    album_title = w[-1]

    # performer_id = insert_performer(artiest, c, conn)
    componist_id = insert_componist(componist, c, conn)
    # instrument_id = insert_instrument(instrument, c, conn)
    album_id = insert_album(
        title=album_title,
        path=cue_path,
        instrument_id=None,  # instrument_id[0],
        performer_id=None,  # performer_id[0],
        componist_id=componist_id[0],
        c=c,
        conn=conn)
    print(files_path)
    [process_file(f) for f in glob.iglob(files_path)]
    for nr, row in enumerate(rows):
        insert_piece(
            name=row['name'],
            code=row['knr'],
            album_id=album_id[0],
            c=c,
            conn=conn)
    conn.close()


def main():
    store_pieces()


if __name__ == '__main__':
    main()
