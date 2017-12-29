import glob

from ..scripts import play_types, filename, kirkpatrick
from . import insert_piece, connect, get_album_path_by_id, \
    delete_pieces_of_album, get_pieces, delete_piece
import os

# from venv.flac.scripts.helper import play_types, filename, kirkpatrick


def refetch_pieces(album_id):
    """
    stukken (pieces en cusheets) opnieuw ophalen
    met behoud van librarycode, dus
    niet opniew ophalen als ze er nog zijn
    :param album_id:
    :return:
    """
    # delete_pieces_of_album(album_id)
    con, c = connect()
    path = get_album_path_by_id(album_id, c)
    insert_or_delete_pieces(path, album_id, con, c)


def insert_or_delete_pieces(path, album_id, conn, c):
    pieces = get_pieces(album_id)
    # delete non-existing pieces
    for p in pieces:
        if not os.path.exists(os.path.join(path, p['Name'])):
            delete_piece(pieces['ID'])
    # insert pieces that exist in directory, not in database
    for card in play_types:
        files_path = u"{}{}".format(path, "/*.{}".format(card))
        for f in glob.iglob(files_path):
            print(f)
            name = filename(f)
            found = False
            for p in pieces:
                if name == p['Name']:
                    found = True
                    break
            if not found:
                insert_piece(
                    name=name,
                    code=kirkpatrick(f),
                    album_id=album_id,
                    c=c,
                    conn=conn)


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
