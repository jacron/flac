from ..services import connect


def get_items_with_id(sql, id):
    conn, c = connect()
    items = [item for item in c.execute(sql, id).fetchall()]
    conn.close()
    return items


def get_items(sql):
    conn, c = connect()
    items = [item for item in c.execute(sql).fetchall()]
    conn.close()
    return items


def get_item_with_id(sql, id):
    conn, c = connect()
    return c.execute(sql, id).fetchone()


def get_albums():
    sql = '''
      SELECT Title, ID from Album
    '''
    return get_items(sql)


def get_pieces(album_id):

    sql = '''
      SELECT Name, File, ID from Piece 
      WHERE AlbumID=?
      ORDER BY Name
    '''
    return get_items_with_id(sql, album_id)


def get_componisten():
    sql = '''
      SELECT FirstName, LastName, ID from Componist
    '''
    return get_items(sql)


def get_performers():
    sql = '''
      SELECT FirstName, LastName, ID from Performer
    '''
    return get_items(sql)


def get_instruments():
    sql = '''
      SELECT Name, ID from Instrument
    '''
    return get_items(sql)


def get_performer_albums(id_performer):
    sql = '''
      SELECT Title, ID from Album
      WHERE PerformerID=?
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
      WHERE ComponistID=?
    '''
    return get_items_with_id(sql, id_componist)


def get_instrument(id_instrument):
    sql = '''
    SELECT * from Instrument WHERE ID=?
    '''
    return get_item_with_id(sql, id_instrument)


def get_componist(id_componist):
    sql = '''
    SELECT * from Componist WHERE ID=?
    '''
    return get_item_with_id(sql, id_componist)


def get_performer(id_performer):
    sql = '''
    SELECT * from Performer WHERE ID=?
    '''
    return get_item_with_id(sql, id_performer)


def get_album(id_album):
    sql = '''
    SELECT * from Album WHERE ID=?
    '''
    return get_item_with_id(sql, id_album)
