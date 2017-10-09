from django.http import HttpResponse
from django.template import loader
from .. import services


def album(request, album_id):
    conn, c = services.connect()
    template = loader.get_template('flac/album.html')

    sql = '''
      SELECT Title, ID from Album WHERE ID=?
    '''
    albumname = c.execute(sql, album_id).fetchone()

    sql = '''
      SELECT Name, File, ID from Piece 
      WHERE AlbumID=?
      ORDER BY Name
    '''
    items = [item for item in c.execute(sql, album_id).fetchall()]
    conn.close()

    context = {
        'items': items,
        'album': albumname,
    }
    return HttpResponse(template.render(context, request))
