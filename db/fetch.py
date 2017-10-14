from .connect import connect


def get_items_with_id(sql, oid):
    conn, c = connect()
    items = [item for item in c.execute(sql, (oid,)).fetchall()]
    conn.close()
    return items


def get_items(sql):
    conn, c = connect()
    items = [item for item in c.execute(sql).fetchall()]
    conn.close()
    return items


def get_item_with_id(sql, oid):
    conn, c = connect()
    return c.execute(sql, (oid,)).fetchone()


def named_albums(items):
    out = []
    for item in items:
        out.append({
            'Title': item[0],
            'ID': item[1],
        })
    return out


def get_albums():
    sql = '''
      SELECT Title, ID from Album
      WHERE IsCollection ISNULL OR IsCollection=0
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items(sql)
    return named_albums(items)


def get_collections():
    sql = '''
      SELECT Title, ID from Album
      WHERE IsCollection=1
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items(sql)
    return named_albums(items)


def get_pieces(album_id):

    sql = '''
      SELECT Name, ID from Piece 
      WHERE AlbumID=?
      ORDER BY Name
    '''
    return get_items_with_id(sql, album_id)


def named_persons(items):
    out = []
    for item in items:
        out.append({
            'FirstName': item[0],
            'LastName': item[1],
            'FullName': u'{} {}'.format(item[0], item[1]),
            'Path': item[2],
            'ID': item[3],
        })
    return out


def get_componisten():
    sql = '''
      SELECT FirstName, LastName, Path, ID from Componist
      ORDER BY LastName
    '''
    items = get_items(sql)
    return named_persons(items)


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
    items = get_items_with_id(sql, id_performer)
    return named_albums(items)


def get_instrument_albums(id_instrument):
    sql = '''
      SELECT Title, ID from Album
      WHERE InstrumentID=?
    '''
    items = get_items_with_id(sql, id_instrument)
    return named_albums(items)


def get_componist_albums(id_componist):
    sql = '''
        SELECT
            Album.Title,
            Album.ID
        FROM Componist_Album
            JOIN Componist ON Componist.ID = Componist_Album.ComponistID
            JOIN Album ON Album.ID = Componist_Album.AlbumID
        WHERE Componist_Album.ComponistID =?
    '''
    # return get_items_with_id(sql, id_componist)
    items = get_items_with_id(sql, id_componist)
    return named_albums(items)


def get_album_albums(id_album):
    sql = '''
      SELECT Title, ID from Album
      WHERE AlbumID=? 
    '''
    items = get_items_with_id(sql, id_album)
    return named_albums(items)


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
    items = get_items_with_id(sql, id_album, )
    out = []
    for item in items:
        out.append({
            'FirstName': item[0],
            'LastName': item[1],
            'FullName': u'{} {}'.format(item[0], item[1]),
            'ID': item[2],
        })
    return out


def get_album_componisten(id_album):
    sql = '''
        SELECT
            FirstName,
            LastName,
            Componist.ID
        FROM Componist_Album
            JOIN Componist ON Componist.ID = Componist_Album.ComponistID
            JOIN Album ON Album.ID = Componist_Album.AlbumID
        WHERE Componist_Album.AlbumID =?
    '''
    items = get_items_with_id(sql, id_album, )
    out = []
    for item in items:
        out.append({
            'FirstName': item[0],
            'LastName': item[1],
            'FullName': u'{} {}'.format(item[0], item[1]),
            'ID': item[2],
        })
    return out


def get_scarlatti_k_pieces():
    sql = '''
      SELECT LibraryCode, Name, Performer.FirstName, Performer.LastName, Performer.ID, Piece.ID 
      from Piece
       join Album
       on Piece.AlbumID = Album.ID
       join Performer_Album
       on Performer_Album.AlbumID = Album.ID
       join Performer
       on Performer_Album.PerformerID = Performer.ID
      WHERE LibraryCode LIKE 'K %'
      ORDER BY LENGTH(LibraryCode), LibraryCode
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'k_code': item[0],
            'Name': item[1],
            'Artiest': '{} {}'.format(item[2], item[3]),
            'ArtiestID': item[4],
            'ID': item[5],
        })
    return out


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
    SELECT Title, Label, Path, ComponistID, AlbumID, ID 
    from Album 
    WHERE Album.ID=?
    '''
    fields = get_item_with_id(sql, id_album)
    return {
        "Title": fields[0],
        "Label": fields[1],
        "Path": fields[2],
        "ComponistID": fields[3],
        "AlbumID": fields[4],
        "ID": fields[5],
    }


def get_mother_title(id_album):
    sql = '''
    SELECT Title 
    from Album 
    WHERE Album.ID=?
    '''
    fields = get_item_with_id(sql, id_album)
    return fields[0]


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
