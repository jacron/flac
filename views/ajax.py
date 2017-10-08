import sqlite3
import os

from django.http import HttpResponse

# from . import services
# import venv.flac.services
# from venv.flac import services

player = '/Applications/Media Center 21.app'


def directory(path):
    p = path.decode('utf-8')
    w = p.split('/')[:-1]
    image_path = '/'.join(w)
    return image_path


def connect():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    return conn, c


def getAlbum(albumId):
    conn, c = connect()
    sql = '''
      SELECT Name, File, ID FROM Piece 
      WHERE AlbumID=?
      ORDER BY Name
    '''
    items = [item for item in c.execute(sql, albumId).fetchall()]
    conn.close()
    return item


def ajax(request):
    if request.POST:
        cmd = request.POST['cmd']
        msg = 'Uitgevoerd cmd: ' + cmd
        if cmd == 'play':
            args = request.POST['arg']
            uargs = args.encode('utf-8')
            os.system('open -a "{}" "{}"'.format(player, uargs))
        if cmd == 'openfinder':
            item = getAlbum(request.POST['arg'])
            path = directory(item[1])
            os.system('open "' + path + '"')
    else:
        msg = 'Dit is geen POST request'
    print(msg)
    return HttpResponse(msg)

