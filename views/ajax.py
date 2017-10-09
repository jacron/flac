import os

from django.http import HttpResponse
from .. import services

player = '/Applications/Media Center 21.app'


def get_album(albumId):
    conn, c = services.connect()
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
            item = get_album(request.POST['arg'])
            path = services.directory(item[1])
            os.system('open "' + path + '"')
    else:
        msg = 'Dit is geen POST request'
    print(msg)
    return HttpResponse(msg)

