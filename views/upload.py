from django.http import HttpResponse
from django.template import loader

from flac.db import get_pieces_nplayed


def uploadalbum(request):
    template = loader.get_template('flac/upload.html')
    return HttpResponse(template.render(
        {
        }, request
    ))


def nplayed(request):
    template = loader.get_template('flac/nplayed.html')
    pieces = get_pieces_nplayed(1)
    return HttpResponse(template.render(
        {
            'items': pieces
        }, request
    ))