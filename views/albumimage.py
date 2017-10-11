from django.http import HttpResponse
from ..db import get_album
from django.conf import settings


def albumimage(request, album_id):
    album = get_album(album_id)
    image_path = album['Path'] + settings.COVER_FILE
    image_path = image_path.encode('utf-8')
    image_data = open(image_path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")
