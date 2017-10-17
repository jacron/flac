from .connect import connect


def get_items_with_id(sql, oid):
    conn, c = connect()
    try:
        items = [item for item in c.execute(sql, (oid,)).fetchall()]
    except:
        print('in db encoding error')
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
    for nr, item in enumerate(items):
        out.append({
            'Title': item[0],
            'ID': item[1],
        })
    return out


def get_album_albums(id_album):
    sql = '''
      SELECT Title, Album.ID, Componist.FirstName, Componist.LastName  
      FROM Album 
      LEFT JOIN Componist_Album ON Componist_Album.AlbumID=Album.ID
      LEFT JOIN Componist ON Componist.ID=Componist_Album.ComponistID
      WHERE Album.AlbumID=?
      GROUP BY Title
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_id(sql, id_album)
    out = []
    for nr, item in enumerate(items):
        componist = ''
        if item[2] or item[3]:
            componist = u'{} {}'.format(item[2], item[3])
        out.append({
            'Title': item[0],
            'ID': item[1],
            'Componist': componist,
        })
    return out


def get_albums():
    sql = '''
      SELECT Title, Album.ID, Componist.FirstName, Componist.LastName  
      FROM Album 
      JOIN Componist_Album ON Album.ID=Componist_Album.AlbumID
      JOIN Componist ON Componist.ID=Componist_Album.ComponistID
      WHERE IsCollection ISNULL OR IsCollection=0
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items(sql)
    out = []
    for nr, item in enumerate(items):
        out.append({
            'Title': item[0],
            'ID': item[1],
            'Componist': u'{} {}'.format(item[2], item[3]),
        })
    return out


def get_collections():
    sql = '''
      SELECT Title, ID FROM Album
      WHERE IsCollection=1
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items(sql)
    return named_albums(items)


def get_gatherers():
    sql = '''
      SELECT Title, ID FROM Album
      WHERE IsCollection=2
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items(sql)
    return named_albums(items)


def get_pieces(album_id):
    sql = '''
      SELECT Name, ID FROM Piece 
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
            'NameFull': u'{}, {}'.format(item[1], item[0]),
            'Path': item[2],
            'Birth': item[3],
            'Death': item[4],
            'ID': item[5],
        })
    return out


def get_componisten():
    sql = '''
      SELECT FirstName, LastName, Path, Birth, Death, ID 
      FROM Componist
      ORDER BY LastName
    '''
    items = get_items(sql)
    return named_persons(items)


def get_performers():
    sql = '''
      SELECT FirstName, LastName, Path, Birth, Death, ID 
      FROM Performer
      ORDER BY LastName
    '''
    items = get_items(sql)
    return named_persons(items)


def get_instruments():
    sql = '''
      SELECT Name, ID 
      FROM Instrument
      ORDER BY Name
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'ID': item[1],
        })
    return out


def get_tags():
    sql = '''
      SELECT Name, ID 
      FROM Tag
      ORDER BY Name
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'ID': item[1],
        })
    return out


def get_performer_albums(id_performer):
    sql = '''
        SELECT
            Album.Title,
            Album.AlbumID,
            Album.ID
        FROM Performer_Album
            JOIN Performer ON Performer.ID = Performer_Album.PerformerID
            JOIN Album ON Album.ID = Performer_Album.AlbumID
        WHERE Performer_Album.PerformerID =?
    '''
    items = get_items_with_id(sql, id_performer)
    named_items = named_albums_with_mother(items)
    return filter_contained_childs(named_items)
    # return named_albums(items)


def get_tag_albums(id_tag):
    sql = '''
        SELECT
            Album.Title,
            Album.AlbumID,
            Album.ID
        FROM Tag_Album
            JOIN Tag ON Tag.ID = Tag_Album.TagID
            JOIN Album ON Album.ID = Tag_Album.AlbumID
        WHERE Tag_Album.TagID =?
    '''
    items = get_items_with_id(sql, id_tag)
    named_items = named_albums_with_mother(items)
    return filter_contained_childs(named_items)
    # return named_albums(items)


def named_albums_with_mother(items):
    out = []
    for item in items:
        out.append({
            'Title': item[0],
            'AlbumID': item[1],
            'ID': item[2],
        })
    return out


def filter_contained_childs(items):
    # filter to get rid of albums that already are contained in a mother album in this list
    filtered = []
    for album in items:
        found = False
        for album2 in items:
            if album2 != album:
                if album2['ID'] == album['AlbumID']:
                    found = True
                    album2['mother'] = True
        if not found:
            filtered.append(album)
    return filtered


def get_instrument_albums(id_instrument):
    sql = '''
      SELECT 
       Title,
       AlbumID,
       ID FROM Album
      WHERE InstrumentID=?
      ORDER BY Title
    '''
    items = get_items_with_id(sql, id_instrument)
    named_items = named_albums_with_mother(items)
    return filter_contained_childs(named_items)


def get_componist_albums(id_componist):
    sql = '''
        SELECT
            Album.Title,
            Album.AlbumID,
            Album.ID
        FROM Componist_Album
            JOIN Componist ON Componist.ID = Componist_Album.ComponistID
            JOIN Album ON Album.ID = Componist_Album.AlbumID
        WHERE Componist_Album.ComponistID =?
        -- AND Album.AlbumID ISNULL 
        -- AND Album.AlbumID NOT IN (MotherID)
        ORDER BY Album.Title
    '''
    items = get_items_with_id(sql, id_componist)
    named_items = named_albums_with_mother(items)
    return filter_contained_childs(named_items)


def get_instrument(id_instrument):
    sql = '''
    SELECT Name FROM Instrument WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_instrument)
    return {
        "Name": fields[0],
    }


def get_componist_path(id_componist):
    sql = '''
    SELECT Path 
    FROM Componist WHERE ID=?
    '''
    return get_item_with_id(sql, id_componist)[0]


def get_componist(id_componist):
    sql = '''
    SELECT FirstName, LastName, Birth, Death, ID 
    FROM Componist WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_componist)
    return {
        "FirstName": fields[0],
        "LastName": fields[1],
        "FullName": u'{} {}'.format(fields[0], fields[1]),
        "Birth": fields[2],
        "Death": fields[3],
        "ID": fields[4],
    }


def get_album_instruments(id_album):
    sql = '''
    SELECT Name, Instrument.ID 
    FROM Instrument
    JOIN Album ON Album.InstrumentID = Instrument.ID
    WHERE Album.ID = ?
    '''
    fields = get_item_with_id(sql, id_album)
    if fields:
        return {
            "Name": fields[0],
            "ID": fields[1],
        }
    else:
        return {}


def get_album_tags(id_album):
    sql = '''
        SELECT
            Name,
            Tag.ID
        FROM Tag_Album
            JOIN Tag ON Tag.ID = Tag_Album.TagID
            JOIN Album ON Album.ID = Tag_Album.AlbumID
        WHERE Tag_Album.AlbumID =?
    '''
    items = get_items_with_id(sql, id_album, )
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'ID': item[1],
        })
    return out


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


def get_scarlatti():
    sql = '''
    SELECT FirstName, LastName, ID
    FROM Componist
    WHERE FirstName='D'
    AND LastName='Scarlatti'
    '''
    conn, c = connect()
    fields = c.execute(sql).fetchone()
    return {
        'FullName': '{} {}'.format(fields[0], fields[1]),
        'ID': fields[2],
    }


def get_scarlatti_k_pieces():
    sql = '''
      SELECT 
        Piece.LibraryCode, 
        Piece.Name, 
        Piece.ID,
        Performer.FirstName, 
        Performer.LastName, 
        Performer.ID, 
        Instrument.Name,
        Instrument.ID
      FROM Piece
       JOIN Album
       ON Piece.AlbumID = Album.ID
       JOIN Performer_Album
       ON Performer_Album.AlbumID = Album.ID
       JOIN Performer
       ON Performer_Album.PerformerID = Performer.ID
       JOIN Instrument
       ON Album.InstrumentID = Instrument.ID
      WHERE LibraryCode LIKE 'K %'
      ORDER BY LENGTH(LibraryCode), LibraryCode
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'k_code': item[0],
            'Piece': {
                'Name': item[1],
                'ID': item[2],
            },
            'Artiest': {
                'Name': u'{} {}'.format(item[3], item[4]),
                'ID': item[5],
            },
            'Instrument': {
                'Name': item[6],
                'ID': item[7],
            },
        })
    return out


def get_performer_path(id_performer):
    sql = '''
    SELECT Path FROM Performer WHERE ID=?
    '''
    return get_item_with_id(sql, id_performer)[0]


def get_tag(id_tag):
    sql = '''
    SELECT Name, ID 
    FROM Tag WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_tag)
    return {
        "Name": fields[0],
        "ID": fields[1],
    }


def get_performer(id_performer):
    sql = '''
    SELECT FirstName, LastName, Birth, Death, ID 
    FROM Performer WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_performer)
    return {
        "FirstName": fields[0],
        "LastName": fields[1],
        "FullName": u'{} {}'.format(fields[0], fields[1]),
        "Birth": fields[2],
        "Death": fields[3],
        "ID": fields[4],
    }


def get_album(id_album):
    sql = '''
    SELECT Title, Label, Path, ComponistID, AlbumID, ID 
    FROM Album 
    WHERE Album.ID=?
    '''
    fields = get_item_with_id(sql, id_album)
    if not fields:
        print(id_album)
        print('has no items')
        return {}
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
    FROM Album 
    WHERE Album.ID=?
    '''
    fields = get_item_with_id(sql, id_album)
    return fields[0]


def get_piece(id_piece):
    sql = '''
    SELECT Name, AlbumID, ID FROM Piece WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_piece)
    return {
        "Name": fields[0],
        "AlbumID": fields[1],
        "ID": fields[2],
    }


def get_album_by_title(title, c, conn):
    sql = '''
    SELECT COUNT(ID) FROM Album
     WHERE Title=?
    '''
    fields = c.execute(sql, (title,)).fetchone()
    return {
        "Count": fields[0],
    }


def get_album_by_path(path, c, conn):
    sql = '''
    SELECT COUNT(ID) FROM Album
     WHERE Path=?
    '''
    fields = c.execute(sql, (path,)).fetchone()
    return {
        "Count": fields[0],
    }
