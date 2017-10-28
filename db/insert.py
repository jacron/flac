from .connect import connect
from ..services import splits_naam


def insert_album(title, path, instrument_id, album_id, is_collectie, c, conn):
    print(title)
    print(path)
    sql = '''
    INSERT OR IGNORE INTO Album
    (Title, InstrumentID, AlbumID, Path, IsCollection) 
    VALUES (?,?,?,?,?)
    '''
    c.execute(sql, (title, instrument_id, album_id, path, is_collectie))
    conn.commit()
    sql = '''
    SELECT ID from Album WHERE Path=?
    '''
    return c.execute(sql, (path,)).fetchone()


def abs_insert_componist(name):
    conn, c = connect()
    return insert_componist(name, c, conn)


def insert_componist(componist, c, conn):
    c_firstname, c_lastname = splits_naam(componist)
    print(c_firstname, c_lastname)
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
    print(name, code, album_id)
    sql = '''
    INSERT OR IGNORE INTO Piece (Name, AlbumID, LibraryCode)
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


def insert_album_performer(performer_id, album_id, c, conn):
    sql = '''
    INSERT OR IGNORE INTO Performer_Album
    (PerformerID, AlbumID)
    VALUES (?,?)
    '''
    c.execute(sql, (performer_id, album_id))
    conn.commit()


def insert_album_componist(componist_id, album_id, c, conn):
    sql = '''
    INSERT OR IGNORE INTO Componist_Album
    (ComponistID, AlbumID)
    VALUES (?,?)
    '''
    c.execute(sql, (componist_id, album_id))
    conn.commit()
