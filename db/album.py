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


