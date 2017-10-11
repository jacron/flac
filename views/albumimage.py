from django.http import HttpResponse
from ..db import get_album


def albumimage(request, album_id):
    album = get_album(album_id)
    image_path = album['Path'] + '/folder.jpg'
    image_path = image_path.encode('utf-8')

    image_data = open(image_path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")
