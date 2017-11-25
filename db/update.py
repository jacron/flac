from flac.db import (get_pieces, get_album_albums,
                     get_album_componisten, get_album_performers, get_album_instruments, insert_componist,
                     insert_album_componist, insert_album_performer, insert_album_instrument)
from .connect import connect
from ..services import splits_naam, splits_years


def get_library_code(name):
    parts = name.split('K. ')
    if len(parts) < 2:
        parts = name.split('K.')
    if len(parts) < 2:
        parts = name.split('KK.')
    if len(parts) < 2:
        return None
    kk = parts[1].split(' ')
    if len(kk) < 2:
        kk = parts[1].split('.')
    if len(kk) < 2:
        kk = parts[1].split(',')
    return 'K ' + kk[0]


def adjust_kk(album_id):
    pieces = get_pieces(album_id)
    for piece in pieces:
        library_code = get_library_code(piece[0])
        if library_code:
            update_piece_library_code(piece[1], library_code)


def inherit_elements(album_id):
    albums = get_album_albums(album_id)
    componisten = get_album_componisten(album_id)
    performers = get_album_performers(album_id)
    instrument = get_album_instruments(album_id)
    conn, c = connect()
    componist_id = componisten[0]['ID']
    performer_id = performers[0]['ID']
    instrument_id = instrument['ID']
    for album in albums:
        insert_album_componist(componist_id, album['ID'], c, conn)
        insert_album_performer(performer_id, album['ID'], c, conn)
        insert_album_instrument(instrument_id, album['ID'], c, conn)


def update_piece_library_code(id, code):
    sql = '''
    UPDATE Piece
    SET LibraryCode=?
    WHERE ID=?
    '''
    con, c = connect()
    c.execute(sql, (code, id, )).fetchone()
    con.commit()


def update_album_title(album_id, title):
    sql = """
    UPDATE Album 
    SET Title=?
    WHERE Album.ID=?
    """
    con, c = connect()
    c.execute(sql, (title, album_id, )).fetchone()
    con.commit()


def add_new_componist_to_album(name, albumid):
    # name is not unambivalently translatable in firstname and lastname
    # so we search for it existing first
    sql = """
    SELECT ID FROM Componist
    WHERE FirstName || ' ' || LastName=?
    """
    con, c = connect()
    componist_id = c.execute(sql, (name, )).fetchone()
    con.close()
    if not componist_id:
        componist_id = new_componist(name)
    if componist_id:
        add_componist_to_album(componist_id[0], albumid)


def add_new_performer_to_album(name, albumid):
    # name is not unambivalently translatable in firstname and lastname
    # so we search for it existing first
    sql = """
    SELECT ID FROM Performer
    WHERE FirstName || ' ' || LastName=?
    """
    con, c = connect()
    performer_id = c.execute(sql, (name, )).fetchone()
    con.close()
    if not performer_id:
        performer_id = new_performer(name)
    if performer_id:
        add_performer_to_album(performer_id[0], albumid)


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


def remove_componist_from_album(componist_id, albumid):
    sql = """
    DELETE FROM Componist_Album
     WHERE ComponistID=? AND AlbumID=?
    """
    con, c = connect()
    c.execute(sql, (componist_id, albumid,)).fetchone()
    con.commit()


def remove_performer_from_album(performer_id, albumid):
    sql = """
    DELETE FROM Performer_Album
     WHERE PerformerID=? AND AlbumID=?
    """
    con, c = connect()
    c.execute(sql, (performer_id, albumid,)).fetchone()
    con.commit()


def remove_instrument_from_album(albumid):
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


def add_new_instrument_to_album(name, albumid):
    print(albumid)
    sql = '''
    SELECT ID FROM Instrument WHERE Name=?
    '''
    con, c = connect()
    instrument_id = c.execute(sql, (name, )).fetchone()
    con.close()
    print(instrument_id)
    if not instrument_id:
        instrument_id = new_instrument(name)
    if instrument_id:
        add_instrument_to_album(instrument_id[0], albumid)



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


def update_componistname(name, componist_id):
    first_name, last_name = splits_naam(name)
    sql = """
    UPDATE Componist
    SET FirstName=?, LastName=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (first_name, last_name, componist_id, )).fetchone()
    con.commit()


def update_componistyears(years, componist_id):
    birth, death = splits_years(years)
    sql = """
    UPDATE Componist
    SET Birth=?, Death=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (birth, death, componist_id, )).fetchone()
    con.commit()


def update_componistbirth(years, componist_id):
    sql = """
    UPDATE Componist
    SET Birth=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (years, componist_id, )).fetchone()
    con.commit()


def update_componistdeath(years, componist_id):
    sql = """
    UPDATE Componist
    SET Death=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (years, componist_id, )).fetchone()
    con.commit()


def update_performerbirth(years, person_id):
    sql = """
    UPDATE Performer
    SET Birth=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (years, person_id,)).fetchone()
    con.commit()


def update_performerdeath(years, person_id):
    sql = """
    UPDATE Performer
    SET Death=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (years, person_id,)).fetchone()
    con.commit()


def update_performername(name, performer_id):
    first_name, last_name = splits_naam(name)
    sql = """
    UPDATE Performer
    SET FirstName=?, LastName=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (first_name, last_name, performer_id,)).fetchone()
    con.commit()


def delete_pieces_of_album(album_id):
    sql = '''
    DELETE FROM Piece
    WHERE AlbumID=?
    '''
    con, c = connect()
    c.execute(sql, (album_id,)).fetchone()
    con.commit()


def delete_album(album_id):
    sql = """
    DELETE FROM Album
    WHERE ID=?"""
    con, c = connect()
    c.execute(sql, (album_id,)).fetchone()
    con.commit()
    sql = """
    DELETE FROM Componist_Album
    WHERE AlbumID=?"""
    con, c = connect()
    c.execute(sql, (album_id,)).fetchone()
    con.commit()


def update_performeryears(years, performer_id):
    birth, death = splits_years(years)
    sql = """
    UPDATE Performer
    SET Birth=?, Death=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (birth, death, performer_id,)).fetchone()
    con.commit()


def add_path_to_componist(componist_id, path):
    sql = """
    UPDATE Componist
    SET Path=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (path, componist_id,)).fetchone()
    con.commit()


def add_path_to_performer(performer_id, path):
    sql = """
    UPDATE Performer
    SET Path=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (path, performer_id,)).fetchone()
    con.commit()


def set_album_title(album_id, title, c, con):
    sql = """
    UPDATE Album 
    SET TITLE=? 
    WHERE ID=?
    """
    c.execute(sql, (title, album_id,)).fetchone()
    con.commit()


def toggle_setting(name):
    sql = """
    UPDATE Settings
    SET VALUE = NOT VALUE 
    WHERE Name=?
    """
    con, c = connect()
    c.execute(sql, (name, )).fetchone()
    con.commit()
