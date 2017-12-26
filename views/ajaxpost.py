import urllib
import os

from flac.services import openpath
from flac.services.album_content import get_website
from flac.services.clipboard import save_score_fragment, save_person
from flac.services.export import export_albums
from flac.services.makecuesheet import make_cuesheet, rename_cuesheet, make_subs_cuesheet, split_cued_file, \
    edit_cuesheet, combine_sub_cuesheets, norm_cuesheet
from flac.services.path import get_path, path_from_id_field
from ..db import (abs_insert_componist, update_componistbirth, update_componistdeath, update_performerbirth,
                  update_performerdeath, adjust_kk, inherit_elements, read_albums)
from flac.db.pieces import refetch_pieces
from ..db import (
    get_album, get_piece, update_album_title, add_tag_to_album,
    add_componist_to_album, add_performer_to_album, add_instrument_to_album,
    add_new_componist_to_album, add_new_performer_to_album, add_new_instrument_to_album,
    remove_tag_from_album, remove_componist_from_album, remove_performer_from_album,
    remove_instrument_from_album,
    new_tag, new_componist, new_performer, new_instrument,
    delete_album,
    update_componistname, update_performername,
)
from django.conf import settings


def play(args):
    piece = get_piece(args)
    album = get_album(piece['AlbumID'])
    path = album['Path'].encode('utf-8')
    name = piece['Name'].encode('utf-8')
    os.system('open -a "{}" "{}"'.format(settings.MEDIA_PLAYER,
                                         "{}/{}".format(path, name)))


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
        openpath(path)


def openwebsite(album_id):
    album = get_album(album_id)
    path = get_website(album['Path'])
    if path:
        openpath(path)


def paste_score_fragment(code):
    return save_score_fragment(code)


def paste_person(id, type):
    return save_person(id, type)


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
        return remove_componist_from_album(post['id'], post['albumid'])
    if cmd == 'update_componist_name':
        return update_componistname(post['name'], post['id'])
    # if cmd == 'update_componist_years':
    #     return update_componistyears(post['years'], post['id'])
    if cmd == 'update_componist_birth':
        return update_componistbirth(post['years'], post['id'])
    if cmd == 'update_componist_death':
        return update_componistdeath(post['years'], post['id'])

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
    # if cmd == 'update_performer_years':
    #     return update_performeryears(post['years'], post['id'])
    if cmd == 'update_performer_birth':
        return update_performerbirth(post['years'], post['id'])
    if cmd == 'update_performer_death':
        return update_performerdeath(post['years'], post['id'])

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
        return refetch_pieces(post['albumid'])
    if cmd == 'read_albums':
        return read_albums(post['albumid'])

    if cmd == 'url':
        person_by_url(post)
        return 'Person image fetched by url'
    if cmd == 'play':
        play(post['arg'])
        return 'Played'
    if cmd == 'openfinder':
        openfinder(post['objectid'], post['kind'])
        return 'Finder opened'
    if cmd == 'exportalbums':
        return export_albums(post['objectid'], post['kind'])
    if cmd == 'openwebsite':
        openwebsite(post['albumid'])
        return 'Website opened'
    if cmd == 'update_album_title':
        return update_album_title(album_id=int(post['albumid']), title=post['title'])
    if cmd == 'adjust_kk':
        return adjust_kk(album_id=int(post['albumid']))
    if cmd == 'inherit_elements':
        return inherit_elements(post['albumid'])

    # cuesheets
    if cmd == 'makecuesheet':
        return make_cuesheet(post['name'], post.getlist('ids[]'), post['albumid'])
    if cmd == 'renamecue':
        return rename_cuesheet(post['id'], post['albumid'])
    if cmd == 'makesubs':
        return make_subs_cuesheet(post['albumid'])
    if cmd == 'split_cued_file':
        return split_cued_file(post['cue_id'], post['albumid'])
    if cmd == 'editcuesheet':
        return edit_cuesheet(post['id'], post['albumid'])
    if cmd == 'combinesubs':
        return combine_sub_cuesheets(post['albumid'])
    if cmd == 'normcuesheet':
        return norm_cuesheet(post['id'], post['albumid'])

    if cmd == 'paste_score_fragment':
        return paste_score_fragment(post['code'])
    if cmd == 'paste_person':
        return paste_person(post['id'],  post['type'])