# coding=utf-8
import json
import os
from django.http import HttpResponse

from flac.services import syspath_performer, syspath_componist
from ..db import (
    get_album, get_piece, update_album_title, add_tag_to_album,
    add_componist_to_album, add_performer_to_album, add_instrument_to_album,
    add_new_componist_to_album, add_new_performer_to_album, add_new_instrument_to_album,
    remove_tag_from_album, remove_componist_from_album, remove_performer_from_album,
    remove_instrument_from_album, get_tags, get_performer, get_componist,
    get_componisten_typeahead, get_performers_typeahead, get_instruments_typeahead,
    new_tag, new_componist, new_performer, new_instrument,
    add_path_to_componist, add_path_to_performer,
    update_componistname, update_componistyears, update_performername, update_performeryears,
)
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


def openfinder_performer(args):
    performer = get_performer(args)
    path = performer['Path']
    if path is None or len(path) == 0:
        path = syspath_performer(performer).encode('utf-8')
        if not os.path.exists(path):
            os.mkdir(path)
        add_path_to_performer(args, path)
    os.system('open "{}"'.format(path))


def openfinder_componist(args):
    componist = get_componist(args)
    path = componist['Path']
    if path is None or len(path) == 0:
        path = syspath_componist(componist).encode('utf-8')
        if not os.path.exists(path):
            os.mkdir(path)
        add_path_to_componist(args, path)
    os.system('open "{}"'.format(path))


def do_update_album_title(title, albumid):
    return update_album_title(album_id=int(albumid), title=title)


def add_componist(componistid, albumid):
    return add_componist_to_album(int(componistid), int(albumid))


def add_new_componist(name, albumid):
    return add_new_componist_to_album(name, int(albumid))


def add_new_performer(name, albumid):
    return add_new_performer_to_album(name, int(albumid))


def add_new_instrument(name, albumid):
    return add_new_instrument_to_album(name, int(albumid))


def get_new_componist(name, albumid):
    componistid = new_componist(name)
    return add_componist_to_album(int(componistid[0]), int(albumid))


def remove_componist(componist_id, albumid):
    return remove_componist_from_album(componist_id, albumid)


def add_performer(performerid, albumid):
    return add_performer_to_album(int(performerid), int(albumid))


def get_new_performer(name, albumid):
    performerid = new_performer(name)
    return add_performer_to_album(int(performerid[0]), int(albumid))


def remove_performer(performer_id, albumid):
    return remove_performer_from_album(performer_id, albumid)


def remove_instrument(albumid):
    return remove_instrument_from_album(albumid)


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


def remove_tag(tag_id, albumid):
    return remove_tag_from_album(tag_id, albumid)


def update_componist_name(name, componist_id):
    return update_componistname(name, componist_id)


def update_componist_years(years, componist_id):
    return update_componistyears(years, componist_id)


def update_performer_name(name, componist_id):
    return update_performername(name, componist_id)


def update_performer_years(years, componist_id):
    return update_performeryears(years, componist_id)


def do_post(post):
    cmd = post['cmd']
    if cmd == 'play':
        play(post['arg'])
        return 'Played'
    if cmd == 'openfinder':
        openfinder(post['arg'])
        return 'Finder opened'
    if cmd == 'openfinder_performer':
        openfinder_performer(post['arg'])
        return 'Finder (performer) opened'
    if cmd == 'openfinder_componist':
        openfinder_componist(post['arg'])
        return 'Finder (componist) opened'
    if cmd == 'update_album_title':
        return do_update_album_title(post['title'], post['albumid'])

    # componist
    if cmd == 'add_componist':
        return add_componist(post['componistid'], post['albumid'])
    if cmd == 'new_componist':
        return get_new_componist(post['name'], post['albumid'])
    if cmd == 'add_new_componist':
        return add_new_componist(post['name'], post['albumid'])
    if cmd == 'remove_componist':
        return remove_componist(post['id'], post['albumid'])
    if cmd == 'update_componist_name':
        return update_componist_name(post['name'], post['id'])
    if cmd == 'update_componist_years':
        return update_componist_years(post['years'], post['id'])

    # performer
    if cmd == 'add_performer':
        return add_performer(post['performerid'], post['albumid'])
    if cmd == 'new_performer':
        return get_new_performer(post['name'], post['albumid'])
    if cmd == 'add_new_performer':
        return add_new_performer(post['name'], post['albumid'])
    if cmd == 'remove_performer':
        return remove_performer(post['id'], post['albumid'])
    if cmd == 'update_performer_name':
        return update_performer_name(post['name'], post['id'])
    if cmd == 'update_performer_years':
        return update_performer_years(post['years'], post['id'])

    # instrument
    if cmd == 'add_instrument':
        return add_instrument(post['instrumentid'], post['albumid'])
    if cmd == 'new_instrument':
        return get_new_instrument(post['name'], post['albumid'])
    if cmd == 'remove_instrument':
        return remove_instrument(post['albumid'])
    if cmd == 'add_new_instrument':
        return add_new_instrument(post['name'], post['albumid'])

    # tag
    if cmd == 'add_tag':
        return add_tag(post['tagid'], post['albumid'])
    if cmd == 'new_tag':
        return get_new_tag(post['name'], post['albumid'])
    if cmd == 'remove_tag':
        return remove_tag(post['id'], post['albumid'])


def do_get(get):
    cmd = get['cmd']
    if cmd == 'tags':
        return json.dumps(get_tags())
    if cmd == 'componisten':
        return json.dumps(get_componisten_typeahead())
    if cmd == 'performers':
        return json.dumps(get_performers_typeahead())
    if cmd == 'instruments':
        return json.dumps(get_instruments_typeahead())
    return 'unknown cmd'


def ajax(request):
    msg = 'No post!'
    if request.POST:
        msg = do_post(request.POST)
    if request.GET:
        msg = do_get(request.GET)
    return HttpResponse(msg)
