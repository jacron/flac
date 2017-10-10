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
    SELECT ID from Performer WHERE FirstName=? AND LastName=?
    '''
    return c.execute(sql, (c_firstname, c_lastname,)).fetchone()


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
