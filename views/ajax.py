# coding=utf-8
import json
import os
from django.http import HttpResponse
from ..db import (
    get_album, get_piece, update_album_title, add_tag_to_album,
    add_componist_to_album, add_performer_to_album, add_instrument_to_album,
    remove_tag_from_album, remove_componist_from_album, remove_performer_from_album,
    remove_instrument_from_album, get_tags,
    new_tag, new_componist, new_performer, new_instrument, )
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


def remove_componist(id, albumid):
    return remove_componist_from_album(id, albumid)


def add_performer(performerid, albumid):
    return add_performer_to_album(int(performerid), int(albumid))


def get_new_performer(name, albumid):
    performerid = new_performer(name)
    return add_performer_to_album(int(performerid[0]), int(albumid))


def remove_performer(id, albumid):
    return remove_performer_from_album(id, albumid)


def remove_instrument(id, albumid):
    return remove_instrument_from_album(id, albumid)


def add_instrument(instrumentid, albumid):
    return add_instrument_to_album(int(instrumentid), int(albumid))


def get_new_instrument(name, albumid):
    instrumentid = new_instrument(name)
    return add_instrument_to_album(int(instrumentid[0]), int(albumid))


def add_tag(tagid, albumid):
    return add_tag_to_album(int(tagid), int(albumid))


def get_new_tag(name, albumid):
    tagid = new_tag(name)
    return add_tag_to_album(int(tagid[0]), int(albumid))


def remove_tag(id, albumid):
    return remove_tag_from_album(id, albumid)


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

    # componist
    if cmd == 'add_componist':
        return add_componist(post['componistid'], post['albumid'])
    if cmd == 'new_componist':
        return get_new_componist(post['name'], post['albumid'])
    if cmd == 'remove_componist':
        return remove_componist(post['id'], post['albumid'])

    # performer
    if cmd == 'add_performer':
        return add_performer(post['performerid'], post['albumid'])
    if cmd == 'new_performer':
        return get_new_performer(post['name'], post['albumid'])
    if cmd == 'remove_performer':
        return remove_performer(post['id'], post['albumid'])

    # instrument
    if cmd == 'add_instrument':
        return add_instrument(post['instrumentid'], post['albumid'])
    if cmd == 'new_instrument':
        return get_new_instrument(post['name'], post['albumid'])
    if cmd == 'remove_instrument':
        return remove_instrument(post['id'], post['albumid'])

    # tag
    if cmd == 'add_tag':
        return add_tag(post['tagid'], post['albumid'])
    if cmd == 'new_tag':
        return get_new_tag(post['name'], post['albumid'])
    if cmd == 'remove_tag':
        return remove_tag(post['id'], post['albumid'])


def do_get(get):
    cmd = get['cmd']
    print(cmd)
    if cmd == 'tags':
        return json.dumps(get_tags())
    return 'unknown cmd'


def ajax(request):
    msg = 'No post!'
    if request.POST:
        msg = do_post(request.POST)
    if request.GET:
        msg = do_get(request.GET)
    return HttpResponse(msg)
