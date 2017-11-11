import urllib
import os
from ..db import (
    abs_insert_componist,
    get_album_path_by_id, connect, insert_piece)
from flac.services import (syspath_performer, syspath_componist, COMPONIST_PATH, filename, trimextension)
from flac.db.pieces import refetch_pieces
from ..db import (
    get_album, get_piece, update_album_title, add_tag_to_album,
    add_componist_to_album, add_performer_to_album, add_instrument_to_album,
    add_new_componist_to_album, add_new_performer_to_album, add_new_instrument_to_album,
    remove_tag_from_album, remove_componist_from_album, remove_performer_from_album,
    remove_instrument_from_album, get_performer, get_componist,
    new_tag, new_componist, new_performer, new_instrument,
    add_path_to_componist, add_path_to_performer,
    delete_album,
    update_componistname, update_componistyears, update_performername, update_performeryears,
)
from django.conf import settings


def create_componist_path(componist_id):
    componist = get_componist(componist_id)
    path = componist['Path']
    if path is None or len(path) == 0:
        path = syspath_componist(componist).encode('utf-8')
        if not os.path.exists(path):
            os.mkdir(path)
        add_path_to_componist(componist_id, path)
    return path


def create_performer_path(performer_id):
    performer = get_performer(performer_id)
    path = performer['Path']
    if path is None or len(path) == 0:
        path = syspath_performer(performer).encode('utf-8')
        if not os.path.exists(path):
            os.mkdir(path)
        add_path_to_performer(performer_id, path)
    return path


def path_from_id_field(post):
    path = None
    componist_id = post.get('componist_id')
    if componist_id:
        path = create_componist_path(componist_id)
    performer_id = post.get('performer_id')
    if performer_id:
        path = create_performer_path(performer_id)
    return path


def write_file_from_url(url, path):
    # r = requests.get(url)
    # u = r.url
    response = urllib.urlretrieve(url)
    contents = open(response[0]).read()
    f = open(path_for_person(path), 'w')
    f.write(contents)
    f.close()


def path_for_person(path):
    return u'{}/person.jpg'.format(path).encode('UTF-8')


def person_by_url(post):
    path = path_from_id_field(post)
    if path:
        write_file_from_url(post['url'], path)


def openfinder_album(args):
    album = get_album(args)
    path = album['Path'].encode('utf-8')
    os.system('open "{}"'.format(path))


def openfinder_performer(args):
    path = create_performer_path(args)
    cmd = u'open "{}"'.format(path).encode('UTF-8')
    os.system(cmd)


def openfinder_componist(args):
    if args is None or len(args) == 0:
        path = COMPONIST_PATH
    else:
        path = create_componist_path(args)
    cmd = u'open "{}"'.format(path).encode('UTF-8')
    os.system(cmd)


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


def do_update_album_title(title, albumid):
    return update_album_title(album_id=int(albumid), title=title)


def update_componist_name(name, componist_id):
    return update_componistname(name, componist_id)


def update_componist_years(years, componist_id):
    return update_componistyears(years, componist_id)


def update_performer_name(name, componist_id):
    return update_performername(name, componist_id)


def update_performer_years(years, componist_id):
    return update_performeryears(years, componist_id)


def delete_album_by_id(album_id):
    return delete_album(album_id)


def play(args):
    piece = get_piece(args)
    album = get_album(piece['AlbumID'])
    path = album['Path'].encode('utf-8')
    name = piece['Name'].encode('utf-8')
    os.system('open -a "{}" "{}"'.format(settings.MEDIA_PLAYER,
                                         "{}/{}".format(path, name)))


def refetch(album_id):
    return refetch_pieces(album_id)


def make_cuesheet(name, ids, album_id):
    conn, cursor = connect()
    path = get_album_path_by_id(album_id, cursor)
    lines = []
    lines.append('TITLE "{}"'.format(name))
    for id in ids:
        piece = get_piece(id)
        fpath = u'{}/{}'.format(path, piece.get('Name'))
        if os.path.exists(fpath):
            print(fpath)
            title = trimextension(filename(fpath))
            lines.append(u'FILE "{}" WAVE'.format(fpath))
            lines.append(u'  TRACK 01 AUDIO')
            lines.append(u'    TITLE "{}"'.format(title))
            lines.append(u'    INDEX 01 00:00:00')
    content = ''
    for line in lines:
        content += line + '\n'
    cuename = u'{}.cue'.format(name)
    wpath = u'{}/{}'.format(path, cuename)
    f = open(wpath, 'w')
    f.write(content)
    f.close()
    insert_piece(
        name=cuename,
        code=0,
        album_id=album_id,
        c=cursor,
        conn=conn)


def do_post(post):
    cmd = post['cmd']
    if cmd == 'url':
        person_by_url(post)
        return 'Person image fetched by url'
    if cmd == 'play':
        play(post['arg'])
        return 'Played'
    if cmd == 'openfinder':
        openfinder_album(post['arg'])
        return 'Finder opened'
    if cmd == 'openfinder_performer':
        openfinder_performer(post['arg'])
        return 'Finder (performer) opened'
    if cmd == 'openfinder_componist':
        openfinder_componist(post['arg'])
        return 'Finder (componist) opened'
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
    if cmd == 'abs_new_componist':
        componist_id = abs_insert_componist(post['name'])
        print(componist_id)
        return componist_id
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

    # album
    if cmd == 'delete_album':
        return delete_album_by_id(post['albumid'])
    if cmd == 'refetch':
        return refetch(post['albumid'])

    # piece
    if cmd == 'makecuesheet':
        return make_cuesheet(post['name'], post.getlist('ids[]'), post['albumid'])
