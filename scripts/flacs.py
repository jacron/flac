"""flac

"""
import glob
import sqlite3
# importing for stand alone script
from venv.flac.services import dirname, filename
from venv.flac.db import insert_album, insert_componist, insert_performer, insert_instrument

cuesheet_extension = '.cue'
flac_wild = "/*.flac"
#           /Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/Sonatas - John Browning - piano
# cue_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/Sonatas - Pierre Hantai - clavecimbel/Sonatas I"
# cue_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/Sonatas - Horowitz  - piano"
cue_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/sonaten piano/Sonatas - John Browning - piano"
flac_path = cue_path + flac_wild
# output_path = "output/scarlatti/"
k_split = " K."
artiest = "Belder"
instrument = "Piano"
rows = []
combine_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/sonaten clavecimbel/Sonatas - Belder/"
combine_part = ["Disc 1of3", "Disc 2of3", "Disc 3of3", ]


def script_connect():
    # let op: het pad naar de database moet relatief zijn, omdat dit script stand alone uitgevoerd wordt!
    db_file = '../../db.sqlite3'
    conn = sqlite3.connect(db_file)
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


def store_row_in_db(filepath, code, album_id, c, conn):
    ffilename = filepath.split('/')[-1]
    filenamesec = ffilename.split('.')[-2]
    sql = '''
    INSERT INTO Piece (Name, AlbumID, File, LibraryCode)
    VALUES (?,?,?,?)
    '''
    c.execute(sql, (filenamesec, album_id, filepath, code))
    conn.commit()


def store_pieces():
    conn, c = script_connect()
    w = cue_path.split('/')
    album_title = w[-1]
    componist = w[-3]

    # print(album_title, componist, artiest)
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

    [process_file(f) for f in glob.iglob(flac_path)]
    for nr, row in enumerate(rows):
        store_row_in_db(row['link_href'], row['knr'], album_id[0], c, conn)
    conn.close()


def combine_file(filepath, nr):
    target = dirname(filepath) + '/' + nr + filename(filepath)
    print(filepath)
    print(target)
    # os.rename(file, target)


def combine():
    nr = '1'
    [combine_file(f, nr) for f in glob.iglob(combine_path + flac_wild)]
    # for album in combine_part:
    #     # print(album)
    #     nr = album.split()[1][0]
    #     # print(nr)
    #     p = combine_path + album + flac_wild
    #     print(p)
    #     [combine_file(f, nr) for f in glob.iglob(p)]


def main():
    store_pieces()
    # combine()

if __name__ == '__main__':
    main()
