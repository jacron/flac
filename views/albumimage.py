from django.http import HttpResponse, HttpResponseNotFound

from flac.settings import BASE_DIR
from ..db import get_album, get_componist_path, get_performer_path
from django.conf import settings
import os


def static_dir(subdir):
    return BASE_DIR + '/flac/static/images/' + subdir


def get_image(path, cached=None):
    image_path = path.encode('utf-8')
    if os.path.exists(image_path):
        image_data = open(image_path, "rb").read()
        if cached:
            fp = open(cached, "wb")
            fp.write(image_data)
        return HttpResponse(image_data, content_type="image/png")
    else:
        return HttpResponse('Dit pad bestaat niet:"{}"'.format(image_path))


def componistimage(request, componist_id):
    cached = static_dir('componist/' + componist_id)
    if os.path.exists(cached):
        print('getting from cache')
        image_data = open(cached, "rb").read()
        return HttpResponse(image_data, content_type="image/png")

    componist_path = get_componist_path(componist_id)
    if not componist_path:
        return empty_response()
    image_path = componist_path + settings.PERSON_FILE
    return get_image(image_path, cached)


def empty_response():
    return HttpResponse()


def instrumentimage(request, instrument_name):
    image_path = '{}{}.jpg'.format(settings.INSTRUMENTS_PATH, instrument_name)
    return get_image(image_path)


def albumimage(request, album_id):
    album = get_album(album_id)
    if not album:
        return HttpResponseNotFound('Dit album bestaat niet:"{}"'.format(album_id), )
    if not album['Path']:
        return empty_response()
    image_path = album['Path'] + settings.COVER_FILE
    return get_image(image_path)


def albumimageback(request, album_id):
    album = get_album(album_id)
    if not album:
        return HttpResponseNotFound('Dit album bestaat niet:"{}"'.format(album_id), )
    if not album['Path']:
        return empty_response()
    image_path = album['Path'] + settings.BACK_FILE
    return get_image(image_path)


def performerimage(request, performer_id):
    performer_path = get_performer_path(performer_id)
    if not performer_path:
        return empty_response()
    image_path = performer_path + settings.PERSON_FILE
    return get_image(image_path)
