import sqlite3

from django.http import HttpResponse, StreamingHttpResponse


def connect():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    return conn, c


def directory(path):
    p = path.decode('utf-8')
    w = p.split('/')[:-1]
    image_path = '/'.join(w)
    return image_path


def albumimage(request, id):
    conn, c = connect()

    sql = '''
      SELECT Name, File, ID from Piece 
      WHERE AlbumID=?
      ORDER BY Name
    '''
    items = [item for item in c.execute(sql, id).fetchall()]
    conn.close()
    image_path = directory(item[1]) + '/folder.jpg'
    upath = image_path.encode('utf-8')[len('file://'):]

    image_data = open(upath, "rb").read()
    return HttpResponse(image_data, content_type="image/png")
