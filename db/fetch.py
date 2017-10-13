from .connect import connect


def get_items_with_id(sql, id):
    conn, c = connect()
    items = [item for item in c.execute(sql, (id,)).fetchall()]
    conn.close()
    return items


def get_items(sql):
    conn, c = connect()
    items = [item for item in c.execute(sql).fetchall()]
    conn.close()
    return items


def get_item_with_id(sql, id):
    conn, c = connect()
    return c.execute(sql, (id,)).fetchone()


def get_albums():
    sql = '''
      SELECT Title, ID from Album
      ORDER BY Title COLLATE NOCASE
    '''
    return get_items(sql)


def get_pieces(album_id):

    sql = '''
      SELECT Name, ID from Piece 
      WHERE AlbumID=?
      ORDER BY Name
    '''
    return get_items_with_id(sql, album_id)


def get_componisten():
    sql = '''
      SELECT FirstName, LastName, Path, ID from Componist
      ORDER BY LastName
    '''
    return get_items(sql)


def get_performers():
    sql = '''
      SELECT FirstName, LastName, Path, ID from Performer
      ORDER BY LastName
    '''
    return get_items(sql)


def get_instruments():
    sql = '''
      SELECT Name, ID from Instrument
    '''
    return get_items(sql)


def get_performer_albums(id_performer):
    sql = '''
        SELECT
            Album.Title,
            Album.ID
        FROM Performer_Album
            JOIN Performer ON Performer.ID = Performer_Album.PerformerID
            JOIN Album ON Album.ID = Performer_Album.AlbumID
        WHERE Performer_Album.PerformerID =?
    '''
    return get_items_with_id(sql, id_performer)


def get_instrument_albums(id_instrument):
    sql = '''
      SELECT Title, ID from Album
      WHERE InstrumentID=?
    '''
    return get_items_with_id(sql, id_instrument)


def get_componist_albums(id_componist):
    sql = '''
      SELECT Title, ID from Album
      WHERE ComponistID=? AND AlbumID ISNULL 
    '''
    return get_items_with_id(sql, id_componist)


def get_album_albums(id_album):
    sql = '''
      SELECT Title, ID from Album
      WHERE AlbumID=? 
    '''
    return get_items_with_id(sql, id_album)


def get_instrument(id_instrument):
    sql = '''
    SELECT Name from Instrument WHERE ID=?
    '''
    return get_item_with_id(sql, id_instrument)


def get_componist(id_componist):
    sql = '''
    SELECT FirstName, LastName, Birth, Death, Path,  ID from Componist WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_componist)
    return {
        "FirstName": fields[0],
        "LastName": fields[1],
        "FullName": u'{} {}'.format(fields[0], fields[1]),
        "Birth": fields[2],
        "Death": fields[3],
        "Path": fields[4],
        "ID": fields[5],
    }


def get_album_performers(id_album):
    sql = '''
        SELECT
            FirstName,
            LastName,
            Performer.ID
        FROM Performer_Album
            JOIN Performer ON Performer.ID = Performer_Album.PerformerID
            JOIN Album ON Album.ID = Performer_Album.AlbumID
        WHERE Performer_Album.AlbumID =?
    '''
    return get_items_with_id(sql, id_album )


def get_performer(id_performer):
    if not id_performer:
        return {}
    # print(id_performer)
    sql = '''
    SELECT FirstName, LastName, Birth, Death, Path, ID from Performer WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_performer)
    return {
        "FirstName": fields[0],
        "LastName": fields[1],
        "FullName": u'{} {}'.format(fields[0], fields[1]),
        "Birth": fields[2],
        "Death": fields[3],
        "Path": fields[4],
        "ID": fields[5],
    }


def get_album(id_album):
    sql = '''
    SELECT Title, Label, Path, ComponistID, ID from Album WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_album)
    return {
        "Title": fields[0],
        "Label": fields[1],
        "Path": fields[2],
        "ComponistID": fields[3],
        "ID": fields[4],
    }


def get_piece(id_piece):
    sql = '''
    SELECT Name, AlbumID, ID from Piece WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_piece)
    return {
        "Name": fields[0],
        "AlbumID": fields[1],
        "ID": fields[2],
    }
