from django.http import HttpResponse
from django.template import loader

from flac.db import get_pianoboeken, get_pianoboek, get_pianoboek_nummers


def list_pianoboeken(request):
    pass


def pianoboek(request, id):
    template = loader.get_template('flac/pianoboek.html')
    return HttpResponse(template.render(
        {
            'pianoboek': get_pianoboek(id),
            'items': get_pianoboek_nummers(id),
        }, request))


def pianoboeken(request):
    template = loader.get_template('flac/pianoboeken.html')
    return HttpResponse(template.render(
        {
            'items': get_pianoboeken()
        }, request))
