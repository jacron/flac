# coding=utf-8
import os
from django.http import HttpResponse
from ..db import (get_album, get_piece, update_album_title,
                  add_componist_to_album, new_componist, )
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


def add_componist(componistid, albumid):
    return add_componist_to_album(int(componistid), int(albumid))


def get_new_componist(name, albumid):
    componistid = new_componist(name)
    return add_componist_to_album(int(componistid[0]), int(albumid))


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
    if cmd == 'add_componist':
        return add_componist(post['componistid'], post['albumid'])
    if cmd == 'new_componist':
        return get_new_componist(post['name'], post['albumid'])


def ajax(request):
    msg = 'No post!'
    if request.POST:
        msg = do_post(request.POST)
    return HttpResponse(msg)
