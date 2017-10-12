import os
from django.http import HttpResponse
from ..db import get_album, get_piece
from django.conf import settings


def play(args):
    piece = get_piece(args)
    album = get_album(piece['AlbumID'])
    path = album['Path'].encode('utf-8')
    os.system('open -a "{}" "{}"'.format(settings.MEDIA_PLAYER,
                                         "{}/{}".format(path, piece['Name'])))


def openfinder(args):
    album = get_album(args)
    path = album['Path'].encode('utf-8')
    os.system('open "{}"'.format(path))


def ajax(request):
    if request.POST:
        cmd = request.POST['cmd']
        arg = request.POST['arg']
        print(arg)
        msg = 'Uitgevoerd cmd: ' + cmd
        if cmd == 'play':
            play(arg)
        if cmd == 'openfinder':
            openfinder(arg)
    else:
        msg = 'Dit is geen POST request'
    print(msg)
    return HttpResponse(msg)
