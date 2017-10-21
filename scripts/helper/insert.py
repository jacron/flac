import glob
from venv.flac.db import (
    insert_componist, insert_performer,
    insert_piece, insert_album_performer, insert_album_componist, )

play_types = ('cue', "flac", "ape", "mp3", "iso", "wma", "wav", "mp3", "m4a", )
k_split = None


def kirkpatrick(filepath):
    if k_split:
        w = filepath.split('/')
        name = w[-1]
        k = name.split(k_split)[1]
        return k.split()[0]
    return 0


def filename(filepath):
    name = filepath.split('/')[-1]
    return name.replace("_", " ")


def insert_pieces(path, album_id, conn, c):
    for card in play_types:
        files_path = u"{}{}".format(path, "/*.{}".format(card))
        for f in glob.iglob(files_path):
            print(f)
            insert_piece(
                name=filename(f),
                code=kirkpatrick(f),
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
