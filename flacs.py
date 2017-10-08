"""flac

"""
import glob
import sqlite3

cuesheet_extension = '.cue'
#           /Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/Sonatas - John Browning - piano
# cue_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/Sonatas - Pierre Hantai - clavecimbel/Sonatas I"
# cue_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/Sonatas - Horowitz  - piano"
cue_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/Sonatas - Belder/Disc 1of3"
flac_path = cue_path + "/*.flac"
# output_path = "output/scarlatti/"
k_split = "- K"
artiest = "Belder"
instrument = "Clavecimbel"
rows = []
# let op: het pad naar de database moet relatief zijn, omdat dit script stand alone uitgevoerd wordt!
db_file = '../db.sqlite3'


def process_file(filepath):
    w = filepath.split('/')
    filename = w[-1]
    nr = filename.split()[0]
    print(filename)
    k = filename.split(k_split)[1]
    knr = k.split()[0]
    rows.append({
        "knr": knr,
        "link_name": artiest + " " + nr,
        "link_href": "file://" + filepath,
    })


def store_row_in_db(filepath, code, album_id, c, conn):
    filename = filepath.split('/')[-1]
    filenamesec = filename.split('.')[-2]
    sql = '''
    INSERT INTO Piece (Name, AlbumID, File, LibraryCode)
    VALUES (?,?,?,?)
    '''
    c.execute(sql, (filenamesec, album_id, filepath, code))
    conn.commit()


def splits_naam(naam, delim):
    c_namen = naam.split(delim)
    if len(c_namen) > 1:
        c_firstname = c_namen[1]
        c_lastname = c_namen[0]
    else:
        c_firstname = ''
        c_lastname = naam
    return c_firstname, c_lastname


def insert_componist(componist, c, conn):
    c_firstname, c_lastname = splits_naam(componist, ',')
    # print(c_firstname, c_lastname)
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


def insert_album(album, performer_id, componist_id, c, conn):
    print(album, performer_id, componist_id)
    sql = '''
    INSERT OR IGNORE INTO Album
    (Title, PerformerID, ComponistID) 
    VALUES (?,?,?)
    '''
    c.execute(sql, (album, performer_id, componist_id))
    conn.commit()
    sql = '''
    SELECT ID from Album WHERE Title=?
    '''
    return c.execute(sql, (album,)).fetchone()


def insert_performer(name, c, conn):
    c_firstname, c_lastname = splits_naam(name, ' ')
    sql = '''
    INSERT OR IGNORE INTO Performer
    (FirstName,LastName) 
    VALUES (?,?)
    '''
    c.execute(sql, (c_firstname, c_lastname))
    conn.commit()
    sql = '''
    SELECT ID from Performer WHERE LastName=?
    '''
    return c.execute(sql, (name,)).fetchone()


def main():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    w = cue_path.split('/')
    album_title = w[-1]
    componist = w[-2]

    print(album_title, componist, artiest)
    performer_id = insert_performer(artiest, c, conn)
    componist_id = insert_componist(componist, c, conn)
    album_id = insert_album(album_title, performer_id[0], componist_id[0], c, conn)

    [process_file(f) for f in glob.iglob(flac_path)]
    for nr, row in enumerate(rows):
        store_row_in_db(row['link_href'], row['knr'], album_id[0], c, conn)
    conn.close()


if __name__ == '__main__':
    main()
