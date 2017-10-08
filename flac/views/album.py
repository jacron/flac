import sqlite3

from django.http import HttpResponse
from django.template import loader


def connect():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    return conn, c


def album(request, id):
    conn, c = connect()
    template = loader.get_template('flac/album.html')

    sql = '''
      SELECT Title, ID from Album WHERE ID=?
    '''
    albumname = c.execute(sql, id).fetchone()

    sql = '''
      SELECT Name, File, ID from Piece 
      WHERE AlbumID=?
      ORDER BY Name
    '''
    items = [item for item in c.execute(sql, id).fetchall()]
    conn.close()

    context = {
        'items': items,
        'album': albumname,
    }
    return HttpResponse(template.render(context, request))
