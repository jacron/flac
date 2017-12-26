from django.http import HttpResponse
from django.template import loader
from ..db import (get_librarycode_sonata, get_librarycode_boek,
                  get_librarycode_sonatas,
                  get_prev_librarycode, get_next_librarycode)


def librarycode_content(librarycode, librarywild):
    prev_id = get_prev_librarycode(librarycode, librarywild)
    next_id = get_next_librarycode(librarycode, librarywild)
    return {
        'pieces': get_librarycode_sonata(librarycode),
        'boeken': get_librarycode_boek(librarycode),
        'librarycode': librarycode,
        'page_title': 'Scarlatti Sonaten ({})'.format(librarycode),
        'prev_id': prev_id,
        'next_id': next_id,
        'wild': librarywild,
    }


def one_librarycode(request, librarycode, librarywild):
    template = loader.get_template('flac/librarycode.html')
    content = librarycode_content(librarycode, librarywild)
    return HttpResponse(template.render(content, request))


def list_librarycode(request, librarywild):
    template = loader.get_template('flac/librarycodes.html')
    return HttpResponse(template.render(
        {
            'items': get_librarycode_sonatas(librarywild),
            'page_title': 'List (' + librarywild + ')',
            'librarywild': librarywild
        }, request))


