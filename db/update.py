from .connect import connect
from ..services import splits_naam


def update_album_title(album_id, title):
    sql = """
    UPDATE Album 
    SET Title=?
    WHERE Album.ID=?
    """
    con, c = connect()
    c.execute(sql, (title, album_id, )).fetchone()
    con.commit()


def add_componist_to_album(componistid, albumid):
    sql = """
    INSERT OR IGNORE INTO Componist_Album 
    (ComponistID, AlbumID)
    VALUES(?,?)
    """
    con, c = connect()
    c.execute(sql, (componistid, albumid, )).fetchone()
    con.commit()


def add_performer_to_album(performerid, albumid):
    sql = """
    INSERT OR IGNORE INTO Performer_Album 
    (PerformerID, AlbumID)
    VALUES(?,?)
    """
    con, c = connect()
    c.execute(sql, (performerid, albumid, )).fetchone()
    con.commit()


def add_tag_to_album(tagid, albumid):
    sql = """
    INSERT OR IGNORE INTO Tag_Album 
    (TagID, AlbumID)
    VALUES(?,?)
    """
    con, c = connect()
    c.execute(sql, (tagid, albumid,)).fetchone()
    con.commit()


def remove_tag_from_album(tagid, albumid):
    sql = """
    DELETE FROM Tag_Album
     WHERE TagID=? AND AlbumID=?
    """
    con, c = connect()
    c.execute(sql, (tagid, albumid,)).fetchone()
    con.commit()


def remove_componist_from_album(id, albumid):
    sql = """
    DELETE FROM Componist_Album
     WHERE ComponistID=? AND AlbumID=?
    """
    con, c = connect()
    c.execute(sql, (id, albumid,)).fetchone()
    con.commit()


def remove_performer_from_album(id, albumid):
    sql = """
    DELETE FROM Performer_Album
     WHERE PerformerID=? AND AlbumID=?
    """
    con, c = connect()
    c.execute(sql, (id, albumid,)).fetchone()
    con.commit()


def remove_instrument_from_album(id, albumid):
    if not albumid:
        print('error')
        return
    sql = """
    UPDATE Album
    SET InstrumentID=NULL 
     WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (albumid,)).fetchone()
    con.commit()


def add_instrument_to_album(instrumentid, albumid):
    sql = """
    UPDATE Album
    SET InstrumentID=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (instrumentid, albumid, )).fetchone()
    con.commit()


def new_componist(name):
    c_firstname, c_lastname = splits_naam(name)
    sql = """
    INSERT OR IGNORE INTO Componist 
    (FirstName, LastName)
    VALUES(?,?)
    """
    con, c = connect()
    c.execute(sql, (c_firstname, c_lastname, )).fetchone()
    con.commit()
    sql = '''
    SELECT ID from Componist WHERE FirstName=? AND LastName=?
    '''
    return c.execute(sql, (c_firstname, c_lastname, )).fetchone()


def new_performer(name):
    c_firstname, c_lastname = splits_naam(name)
    sql = """
    INSERT OR IGNORE INTO Performer 
    (FirstName, LastName)
    VALUES(?,?)
    """
    con, c = connect()
    c.execute(sql, (c_firstname, c_lastname, )).fetchone()
    con.commit()
    sql = '''
    SELECT ID from Performer WHERE FirstName=? AND LastName=?
    '''
    return c.execute(sql, (c_firstname, c_lastname, )).fetchone()


def new_tag(name):
    sql = """
    INSERT OR IGNORE INTO Tag 
    (Name)
    VALUES(?)
    """
    con, c = connect()
    c.execute(sql, (name, )).fetchone()
    con.commit()
    sql = '''
    SELECT ID from Tag WHERE Name=?
    '''
    return c.execute(sql, (name, )).fetchone()


def new_instrument(name):
    sql = """
    INSERT OR IGNORE INTO Instrument 
    (Name)
    VALUES(?)
    """
    con, c = connect()
    c.execute(sql, (name, )).fetchone()
    con.commit()
    sql = '''
    SELECT ID from Instrument WHERE Name=?
    '''
    return c.execute(sql, (name, )).fetchone()
