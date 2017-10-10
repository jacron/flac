from ..services import connect


def get_albums():
    conn, c = connect()
    sql = '''
      SELECT Title, ID from Album
    '''
    albums = [item for item in c.execute(sql).fetchall()]
    conn.close()
    return albums


def get_componisten():
    conn, c = connect()
    sql = '''
      SELECT FirstName, LastName, ID from Componist
    '''
    items = [item for item in c.execute(sql).fetchall()]
    conn.close()
    return items
