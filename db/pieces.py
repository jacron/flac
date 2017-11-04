import glob

# from ..db import insert_piece
from . import insert_piece, connect, get_album_path_by_id, delete_pieces_of_album
from flac.scripts.helper.insert import play_types, filename, kirkpatrick


def refetch_pieces(album_id):
    delete_pieces_of_album(album_id)
    con, c = connect()
    path = get_album_path_by_id(album_id, c)
    insert_pieces(path, album_id, con, c)


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







