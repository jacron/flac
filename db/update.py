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
    ret = c.execute(sql, (componistid, albumid, )).fetchone()
    print(ret)
    con.commit()


def new_componist(name):
    c_firstname, c_lastname = splits_naam(name)
    sql = """
    INSERT OR IGNORE INTO Componist 
    (FirstName, LastName)
    VALUES(?,?)
    """
    con, c = connect()
    ret = c.execute(sql, (c_firstname, c_lastname, )).fetchone()
    print(ret)
    con.commit()
