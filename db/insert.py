from ..services import splits_naam


def insert_album(title, path, instrument_id, performer_id, componist_id, c, conn):
    print('+++')
    print(title, performer_id, componist_id, instrument_id, path)
    # return
    sql = '''
    INSERT OR IGNORE INTO Album
    (Title, InstrumentID, PerformerID, ComponistID, Path) 
    VALUES (?,?,?,?,?)
    '''
    c.execute(sql, (title, instrument_id, performer_id, componist_id, path))
    conn.commit()
    sql = '''
    SELECT ID from Album WHERE Title=?
    '''
    return c.execute(sql, (title,)).fetchone()


def insert_componist(componist, c, conn):
    c_firstname, c_lastname = splits_naam(componist)
    sql = '''
    INSERT OR IGNORE INTO Componist 
    (FirstName, LastName) 
    VALUES (?,?)
    '''
    c.execute(sql, (c_firstname, c_lastname))
    conn.commit()
    sql = '''
    SELECT ID from Componist WHERE FirstName=? AND LastName=?
    '''
    return c.execute(sql, (c_firstname, c_lastname)).fetchone()


def insert_piece(name, code, album_id, c, conn):
    sql = '''
    INSERT INTO Piece (Name, AlbumID, LibraryCode)
    VALUES (?,?,?)
    '''
    c.execute(sql, (name, album_id, code))
    conn.commit()


def insert_instrument(name, c, conn):
    sql = '''
    INSERT OR IGNORE INTO Instrument
    (Name) 
    VALUES (?)
    '''
    c.execute(sql, (name, ))
    conn.commit()
    sql = '''
    SELECT ID from Instrument WHERE Name=?
    '''
    return c.execute(sql, (name,)).fetchone()


def insert_performer(name, c, conn):
    c_firstname, c_lastname = splits_naam(name)
    sql = '''
    INSERT OR IGNORE INTO Performer
    (FirstName,LastName) 
    VALUES (?,?)
    '''
    c.execute(sql, (c_firstname, c_lastname))
    conn.commit()
    sql = '''
    SELECT ID from Performer WHERE FirstName=? AND LastName=?
    '''
    return c.execute(sql, (c_firstname, c_lastname,)).fetchone()


