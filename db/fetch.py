from .connect import connect


def make_fullname(FirstName, LastName):
    if not FirstName or len(FirstName) == 0:
        return LastName
    return u'{} {}'.format(FirstName, LastName)


def get_items_with_parameter(sql, oid):
    conn, c = connect()
    items = []
    try:
        items = [item for item in c.execute(sql, (oid,)).fetchall()]
    except:
        print('in db encoding error')
    conn.close()
    return items


def get_items_with_2parameter(sql, a, b):
    conn, c = connect()
    items = []
    try:
        items = [item for item in c.execute(sql, (a, b, )).fetchall()]
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
      SELECT 
      Title, 
      Album.ID, 
      Componist.FirstName, 
      Componist.LastName  
      FROM Album 
      LEFT JOIN Componist_Album ON Componist_Album.AlbumID=Album.ID
      LEFT JOIN Componist ON Componist.ID=Componist_Album.ComponistID
      WHERE Album.AlbumID=?
      GROUP BY Title
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, id_album)
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


sqlAllAlbums = '''
      SELECT 
      Title, 
      Album.ID
      FROM Album 
      WHERE Album.AlbumID=?
      GROUP BY Title
      ORDER BY Title COLLATE NOCASE
    '''


def get_next_album(id_mother, id_album):
    if not id_mother : return None
    items = get_items_with_parameter(sqlAllAlbums, id_mother)
    match = None
    for item in items:
        if match:
            return item[1]
        if int(item[1]) == int(id_album):
            match = id_album
    return None


def get_prev_album(id_mother, id_album):
    if not id_mother : return None
    items = get_items_with_parameter(sqlAllAlbums, id_mother)
    match = None
    for item in items:
        if match and int(item[1]) == int(id_album):
            return match
        match = int(item[1])
    return None


def get_albums_by_title(q):
    sql = '''
      SELECT Title, Album.ID, Componist.FirstName, Componist.LastName  
      FROM Album 
      JOIN Componist_Album ON Album.ID=Componist_Album.AlbumID
      JOIN Componist ON Componist.ID=Componist_Album.ComponistID
      WHERE Title LIKE ?
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, '%' + q + '%')
    out = []
    for nr, item in enumerate(items):
        out.append({
            'Title': item[0],
            'ID': item[1],
            'Componist': u'{} {}'.format(item[2], item[3]),
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
    return get_items_with_parameter(sql, album_id)


def named_persons(items):
    out = []
    for item in items:
        out.append({
            'FirstName': item[0],
            'LastName': item[1],
            'FullName': make_fullname(item[0], item[1]),
            'NameFull': u'{}, {}'.format(item[1], item[0]),
            'Path': item[2],
            'Birth': item[3],
            'Death': item[4],
            'ID': item[5],
            'Albums': item[6],
        })
    return out


def get_componisten_typeahead():
    sql = '''
      SELECT FirstName, LastName, ID
      FROM Componist
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'FullName': make_fullname(item[0], item[1]),
            'ID': item[2],
        })
    return out


def get_performers_typeahead():
    sql = '''
      SELECT FirstName, LastName, ID
      FROM Performer
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'FullName': make_fullname(item[0], item[1]),
            'ID': item[2],
        })
    return out


def get_general_search(query):
    # get album by name, as a simple beginning
    sql = '''
      SELECT Title, ID
      FROM Album
      WHERE Album.Title LIKE ?
      LIMIT 10
    '''
    items = get_items_with_parameter(sql, '%' + query + '%')
    out = []
    for item in items:
        # out.append(item[0])
        out.append({
            'name': item[0],
            'ID': item[1],
        })
    return out


def get_instruments_typeahead():
    sql = '''
      SELECT Name, ID
      FROM Instrument
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'ID': item[1],
        })
    return out


def get_period_componisten(period):
    # print('period={}'.format(period))
    pp = period.split('-')
    if len(pp) == 1:
        pmin = period
        pmax = 0
    else:
        if len(pp[0]) < 1:  # e.g. -1900
            pmin = 0
            pmax = pp[1]
        else:
            if len(pp[1]) < 1:  # e.g. 1800-
                pmin = pp[0]
                pmax = 0
            else:
                pmin = pp[0]
                pmax = pp[1]
    sql = '''
    SELECT *
    FROM (
      SELECT
        FirstName,
        LastName,
        C.Path,
        Birth,
        Death,
        C.ID,
        COUNT(A.ID) AS Albums
      FROM Componist C
        LEFT JOIN Componist_Album CA
          ON CA.ComponistID = C.ID
         LEFT JOIN Album A
          ON CA.AlbumID = A.ID
      GROUP BY C.ID
      ORDER BY LastName
    ) WHERE Death > ?
    '''
    if pmax > 0:
        sql += 'AND Death < ?'
        items = get_items_with_2parameter(sql, int(pmin), int(pmax))
    else:
        items = get_items_with_parameter(sql, int(pmin))
    return named_persons(items)


def get_componisten(limit=0):
    sql = '''
SELECT *
FROM (
  SELECT
    FirstName,
    LastName,
    C.Path,
    Birth,
    Death,
    C.ID,
    COUNT(A.ID) AS Albums
  FROM Componist C
    LEFT JOIN Componist_Album CA
      ON CA.ComponistID = C.ID
     LEFT JOIN Album A
      ON CA.AlbumID = A.ID
  GROUP BY C.ID
  ORDER BY LastName
)
-- WHERE Albums > ?
'''
    # items = get_items_with_parameter(sql, int(limit))
    items = get_items(sql)
    return named_persons(items)


def get_performers():
    sql = '''
      SELECT FirstName, LastName, C.Path, Birth, Death,
        C.ID, COUNT(A.ID) AS Albums
      FROM Performer C
        LEFT JOIN Performer_Album CA
          ON CA.PerformerID = C.ID
        LEFT JOIN Album A
          ON CA.AlbumID = A.ID
      GROUP BY C.ID
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


def get_componist_aliasses():
    sql = '''
      SELECT Name, ComponistID 
      FROM ComponistAlias
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'ComponistID': item[1],
        })
    return out


def get_performer_aliasses():
    sql = '''
      SELECT Name, PerformerID
      FROM PerformerAlias
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'PerformerID': item[1],
        })
    return out


def get_tags():
    sql = '''
      SELECT Name, ID 
      FROM Tag
      ORDER BY Name COLLATE NOCASE
    '''
    items = get_items(sql)
    out = []
    len = 0
    for item in items:
        len += 1
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
        ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, id_performer)
    named_items = named_albums_with_mother(items)
    return filter_contained_children(named_items)
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
        ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, id_tag)
    named_items = named_albums_with_mother(items)
    return filter_contained_children(named_items)
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


def filter_contained_children(items):
    # return lists of mothers (with property mother is true) and children
    # N.B. sometimes a mother is a child, i.e. in the children list an album has property mother true
    # but somehow this is right
    # Title, AlbumID, ID
    children = []
    mothers = []
    for album1 in items:
        found = False
        for album2 in items:
            if album2 != album1:
                if album2['ID'] == album1['AlbumID']: # this album has a mother in this list
                    found = True
                    album2['mother'] = True
        if not found:
            if album1.get('mother'):
                mothers.append(album1)
            else:
                children.append(album1)
    for album in children:
        if album.get('mother'):
            mothers.append(album)
            children.remove(album)
    return {
        'mothers': sorted(mothers, key=lambda album: album['Title'].lower),
        'children': children
    }


def get_instrument_albums(id_instrument):
    sql = '''
      SELECT 
       Title,
       AlbumID,
       ID FROM Album
      WHERE InstrumentID=?
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, id_instrument)
    named_items = named_albums_with_mother(items)
    return filter_contained_children(named_items)


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
        ORDER BY Album.Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, id_componist)
    named_items = named_albums_with_mother(items)
    return filter_contained_children(named_items)


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
    SELECT FirstName, LastName, Birth, Death, Path, ID 
    FROM Componist WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_componist)
    return {
        "FirstName": fields[0],
        "LastName": fields[1],
        "FullName": make_fullname(fields[0], fields[1]),
        "Birth": fields[2],
        "Death": fields[3],
        "Path": fields[4],
        "ID": fields[5],
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
    items = get_items_with_parameter(sql, id_album, )
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
    items = get_items_with_parameter(sql, id_album, )
    out = []
    for item in items:
        out.append({
            'FirstName': item[0],
            'LastName': item[1],
            'FullName': make_fullname(item[0], item[1]),
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
    items = get_items_with_parameter(sql, id_album, )
    out = []
    for item in items:
        out.append({
            'FirstName': item[0],
            'LastName': item[1],
            'FullName': make_fullname(item[0], item[1]),
            'ID': item[2],
        })
    return out


def get_setting(name):
    sql = '''
    SELECT VALUE
    FROM Settings
    WHERE Name=?
    '''
    conn, c = connect()
    fields = c.execute(sql, (name, )).fetchone()
    return {
        'VALUE': fields[0],
    }


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
        'FullName': make_fullname(fields[0], fields[1]),
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
    SELECT FirstName, LastName, Birth, Death, Path, ID 
    FROM Performer WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_performer)
    return {
        "FirstName": fields[0],
        "LastName": fields[1],
        "FullName": make_fullname(fields[0], fields[1]),
        "Birth": fields[2],
        "Death": fields[3],
        "Path": fields[4],
        "ID": fields[5],
    }


def get_album_path_by_id(album_id, c):
    sql = '''
    SELECT Path 
    FROM Album 
    WHERE Album.ID=?
    '''
    fields = c.execute(sql, (album_id,)).fetchone()
    if not fields:
        print('ID not found')
        return None
    return fields[0]


def get_componist_path_by_id(componist_id, c):
    sql = '''
    SELECT Path 
    FROM Componist 
    WHERE ID=?
    '''
    fields = c.execute(sql, (componist_id,)).fetchone()
    return fields[0]


def get_componist_id_from_album(album_id, c):
    sql = '''
    SELECT ComponistID 
    FROM Componist_Album 
    WHERE AlbumID=?
    '''
    fields = c.execute(sql, (album_id,)).fetchone()
    return fields[0]


def get_album(id_album):
    sql = '''
    SELECT Title, Label, Path, AlbumID, ID 
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
        "AlbumID": fields[3],
        "ID": fields[4],
    }


def get_componist_path_c(componist_id, c):
    sql = '''
    SELECT Path
    FROM Componist
    WHERE ID=?
    '''
    fields = c.execute(sql, (componist_id,)).fetchone()
    return fields[0]


def get_album_by_path(path, c, conn):
    sql = '''
    SELECT Title, Label, Path, AlbumID, ID 
    FROM Album 
    WHERE Album.Path=?
    '''
    fields = c.execute(sql, (path,)).fetchone()
    if not fields:
        print(path)
        print('has no items')
        return {}
    return {
        "Title": fields[0],
        "Label": fields[1],
        "Path": fields[2],
        "AlbumID": fields[3],
        "ID": fields[4],
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


def get_album_count_by_path(path, c, conn):
    sql = '''
    SELECT COUNT(ID) FROM Album
     WHERE Path=?
    '''
    fields = c.execute(sql, (path,)).fetchone()
    return {
        "Count": fields[0],
    }
