from django.http import HttpResponse
from ..db import get_album, get_componist, get_performer
from django.conf import settings
import os


def get_image(path):
    image_path = path.encode('utf-8')
    if os.path.exists(image_path):
        image_data = open(image_path, "rb").read()
        return HttpResponse(image_data, content_type="image/png")
    else:
        return HttpResponse('Dit pad bestaat niet:"{}"'.format(image_path))


def albumimage(request, album_id):
    album = get_album(album_id)
    image_path = album['Path'] + settings.COVER_FILE
    return get_image(image_path)


def componistimage(request, componist_id):
    componist = get_componist(componist_id)
    image_path = componist['Path'] + settings.PERSON_FILE
    return get_image(image_path)


def performerimage(request, performer_id):
    performer = get_performer(performer_id)
    image_path = performer['Path'] + settings.PERSON_FILE
    return get_image(image_path)
