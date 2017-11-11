import urllib
import os

from flac.services.makecuesheet import make_cuesheet, rename_cuesheet
from flac.services.path import get_path, path_from_id_field
from ..db import (abs_insert_componist, )
from flac.db.pieces import refetch_pieces
from ..db import (
    get_album, get_piece, update_album_title, add_tag_to_album,
    add_componist_to_album, add_performer_to_album, add_instrument_to_album,
    add_new_componist_to_album, add_new_performer_to_album, add_new_instrument_to_album,
    remove_tag_from_album, remove_componist_from_album, remove_performer_from_album,
    remove_instrument_from_album,
    new_tag, new_componist, new_performer, new_instrument,
    delete_album,
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


def refetch(album_id):
    return refetch_pieces(album_id)


def path_for_person(path):
    return u'{}/person.jpg'.format(path).encode('UTF-8')


def write_file_from_url(url, path):
    response = urllib.urlretrieve(url)
    contents = open(response[0]).read()
    f = open(path_for_person(path), 'w')
    f.write(contents)
    f.close()


def person_by_url(post):
    path = path_from_id_field(post)
    if path:
        write_file_from_url(post['url'], path)


def openfinder(objectid, kind):
    path = get_path(objectid, kind)
    if path:
        cmd = u'open "{}"'.format(path).encode('UTF-8')
        os.system(cmd)


def do_post(post):
    cmd = post['cmd']

    # componist
    if cmd == 'add_componist':
        return add_componist_to_album(int(post['componistid']), int(post['albumid']))
    if cmd == 'new_componist':
        componistid = new_componist(post['name'])
        return add_componist_to_album(int(componistid[0]), int(post['albumid']))
    if cmd == 'add_new_componist':
        return add_new_componist_to_album(post['name'], int(post['albumid']))
    if cmd == 'abs_new_componist':
        componist_id = abs_insert_componist(post['name'])
        print(componist_id)
        return componist_id
    if cmd == 'remove_componist':
        return remove_componist_from_album(post['componist_id'], post['albumid'])
    if cmd == 'update_componist_name':
        return update_componistname(post['name'], post['id'])
    if cmd == 'update_componist_years':
        return update_componistyears(post['years'], post['id'])

    # performer
    if cmd == 'add_performer':
        return add_performer_to_album(int(post['performerid']), int(post['albumid']))
    if cmd == 'new_performer':
        performerid = new_performer(post['name'])
        return add_performer_to_album(int(performerid[0]), int(post['albumid']))
    if cmd == 'add_new_performer':
        return add_new_performer_to_album(post['name'], int(post['albumid']))
    if cmd == 'remove_performer':
        return remove_performer_from_album(post['id'], post['albumid'])
    if cmd == 'update_performer_name':
        return update_performername(post['name'], post['id'])
    if cmd == 'update_performer_years':
        return update_performeryears(post['years'], post['id'])

    # instrument
    if cmd == 'add_instrument':
        return add_instrument_to_album(int(post['instrumentid']), int(post['albumid']))
    if cmd == 'new_instrument':
        instrumentid = new_instrument(post['name'])
        return add_instrument_to_album(int(instrumentid[0]), int(post['albumid']))
    if cmd == 'remove_instrument':
        return remove_instrument_from_album(post['albumid'])
    if cmd == 'add_new_instrument':
        return add_new_instrument_to_album(post['name'], int(post['albumid']))

    # tag
    if cmd == 'add_tag':
        return add_tag_to_album(int(post['tagid']), int(post['albumid']))
    if cmd == 'new_tag':
        tagid = new_tag(post['name'])
        return add_tag_to_album(int(tagid[0]), int(post['albumid']))
    if cmd == 'remove_tag':
        return remove_tag_from_album(post['id'], post['albumid'])

    # album
    if cmd == 'delete_album':
        return delete_album(post['album_id'])
    if cmd == 'refetch':
        return refetch(post['albumid'])

    if cmd == 'url':
        person_by_url(post)
        return 'Person image fetched by url'
    if cmd == 'play':
        play(post['arg'])
        return 'Played'
    if cmd == 'openfinder':
        openfinder(post['objectid'], post['kind'])
        return 'Finder opened'
    if cmd == 'update_album_title':
        return update_album_title(album_id=int(post['albumid']), title=post['title'])

    # piece
    if cmd == 'makecuesheet':
        return make_cuesheet(post['name'], post.getlist('ids[]'), post['albumid'])
    if cmd == 'renamecue':
        return rename_cuesheet(post['id'], post['albumid'])
