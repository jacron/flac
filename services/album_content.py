# coding: utf-8
import glob
import os

from flac.services.proposals import get_proposals, get_artists
from flac.services.tag import get_metatags
from flac.settings import SKIP_DIRS
from ..db import (
    get_album, get_pieces,
    get_mother_title, get_album_albums, get_album_componisten, get_album_performers, get_album_instruments,
    get_album_tags, get_setting, get_prev_album, get_next_album, get_prev_list_album,
    get_next_list_album, get_componist, get_performer, get_tag, get_path_doubles)
from ..services import get_full_cuesheet


def has_notfound_files(cuesheet, album_path):
    # for file in cuesheet['cue']['files']:
        # fname = file['name'].encode('utf-8')
        # path = '{}/{}'.format(album_path, fname)
        # if not os.path.exists(path):
        #     return True
    # return False
    pass


def organize_pieces(album_id, album_path):
    items = get_pieces(album_id)
    cuesheets, pieces, notfounds, invalidcues = [], [], [], []
    album_metatags = []
    for item in items:
        ffile = item[0]
        if ffile:
            path = u'{}/{}'.format(album_path, ffile)
            if os.path.exists(path):
                extension = ffile.split('.')[-1]
                if extension == 'cue':
                    cuesheet = get_full_cuesheet(path, item[1])
                    if has_notfound_files(cuesheet, album_path):
                        invalidcues.append(cuesheet)
                    else:
                        cuesheet['Code'] = item[2]
                        cuesheets.append(cuesheet)
                else:
                    item['tags'] = get_metatags(path)
                    album_metatags = item['tags']
                    pieces.append(item)
            else:
                notfounds.append(path)
    return cuesheets, pieces, notfounds, invalidcues, album_metatags


def check_subdirs(path):
    for d in os.listdir(path):
        p = os.path.join(path, d)
        if os.path.isdir(p) and d not in SKIP_DIRS:
            return True
    return False


def get_title_for_list(list_name, list_id):
    person = None
    if list_name == 'componist':
        person = get_componist(list_id)
    if list_name == 'performer':
        person = get_performer(list_id)
    if person:
        return person['FullName']
    if list_name == 'tag':
        return get_tag(list_id)['Name']
    if list_name == 'gather':
        return 'verzamelalbums'


def get_elements(album_id):
    return get_album_componisten(album_id), get_album_performers(album_id), get_album_instruments(album_id)


def get_website(path):
    website_path = os.path.join(path, 'website')
    if os.path.exists(website_path):
        for f in glob.iglob(os.path.join(website_path, '*.html')):
            return f
        for f in glob.iglob(os.path.join(website_path, '*.htm')):
            return f
    return None


def album_paging(mother_id, album_id):
    prev_id = get_prev_album(mother_id, album_id)
    next_id = get_next_album(mother_id, album_id)
    return prev_id, next_id


def list_paging(album_id, list_name, list_id):
    next_list_id = get_next_list_album(album_id, list_name, list_id)
    prev_list_id = get_prev_list_album(album_id, list_name, list_id)
    if next_list_id:
        next_list_id = '{}/{}/{}/'.format(next_list_id, list_name, list_id)
    if prev_list_id:
        prev_list_id = '{}/{}/{}/'.format(prev_list_id, list_name, list_id)
    list_title = None
    if next_list_id or prev_list_id:
        list_title = get_title_for_list(list_name, list_id)
    return next_list_id, prev_list_id, list_title


def images_album(album_o):
    album_folder_image, album_back_image = None, None
    path = os.path.join(album_o['Path'], 'folder.jpg')
    if os.path.exists(path):
        album_folder_image = True
    path = os.path.join(album_o['Path'], 'back.jpg')
    if os.path.exists(path):
        album_back_image = True
    return album_folder_image, album_back_image


def album_context(album_id, list_name=None, list_id=None):
    album_o = get_album(album_id)
    if not album_o:
        return None
    mother_title, mother_id = None, None
    album_o = get_album(album_id)
    if album_o['AlbumID']:
        mother_id = album_o['AlbumID']
        mother_title = get_mother_title(mother_id)
    cuesheets, pieces, notfounds, invalidcues, album_metatags = organize_pieces(album_id, album_o['Path'])
    album_componisten, album_performers, album_instruments = get_elements(album_id)
    sp = get_setting('show_proposals')
    show_proposals = sp['VALUE']
    proposals, artists = [], []
    if show_proposals == '1':
        allsheets = cuesheets + invalidcues
        proposals = get_proposals(allsheets, pieces, album_o, album_componisten)
        artists = get_artists(allsheets, pieces, album_o, album_performers)
    next_list_id, prev_list_id, list_title = list_paging(album_id, list_name, list_id)
    prev_id, next_id = album_paging(mother_id, album_id)  # for collections
    album_folder_image, album_back_image = images_album(album_o)
    return {
        'albumid': album_id,
        'album_folder_image': album_folder_image,
        'album_back_image': album_back_image,
        'pieces': pieces,
        'albums': get_album_albums(album_id),
        'album': album_o,
        'mother_title': mother_title,
        'album_componisten': album_componisten,
        'album_performers': album_performers,
        'album_instrument': album_instruments,
        'cuesheets': cuesheets,
        'invalidcues': invalidcues,
        'notfounds': notfounds,
        'album_tags': get_album_tags(album_id),
        'album_metatags': album_metatags,
        'proposals': proposals,
        'show_proposals': show_proposals,
        'artists': artists,
        'prev_id': prev_id,
        'next_id': next_id,
        'prev_list_id': prev_list_id,
        'next_list_id': next_list_id,
        'list_name': list_name,
        'list_title': list_title,
        'list_id': list_id,
        'has_subdirs': check_subdirs(album_o['Path']),
        'website': get_website(album_o['Path']),
        'path_doubles': get_path_doubles(album_o)
    }
