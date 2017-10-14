# coding=utf-8
import os
from django.http import HttpResponse
from ..db import get_album, get_piece, update_album_title
from django.conf import settings


def play(args):
    piece = get_piece(args)
    album = get_album(piece['AlbumID'])
    path = album['Path'].encode('utf-8')
    name = piece['Name'].encode('utf-8')
    os.system('open -a "{}" "{}"'.format(settings.MEDIA_PLAYER,
                                         "{}/{}".format(path, name)))


def openfinder(args):
    album = get_album(args)
    path = album['Path'].encode('utf-8')
    os.system('open "{}"'.format(path))


def do_update_album_title(title, albumid):
    return update_album_title(album_id=int(albumid), title=title)


def do_post(post):
    cmd = post['cmd']
    if cmd == 'play':
        play(post['arg'])
        return 'Played'
    if cmd == 'openfinder':
        openfinder(post['arg'])
        return 'Finder opened'
    if cmd == 'update_album_title':
        return do_update_album_title(post['title'], post['albumid'])


def ajax(request):
    msg = 'No post!'
    if request.POST:
        msg = do_post(request.POST)
    return HttpResponse(msg)
