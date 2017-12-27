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
        'prev_id': prev_id,
        'next_id': next_id,
        'wild': librarywild,
    }


def one_librarycode(request, librarycode, librarywild='dummy'):
    template = loader.get_template('flac/librarycode.html')
    content = librarycode_content(librarycode, librarywild)
    return HttpResponse(template.render(content, request))


def get_full_items(librarywild):
    items = get_librarycode_sonatas(librarywild)
    for item in items:
        item['pieces'] = get_librarycode_sonata(item['k_code'])
        item['pianoboeken'] = get_librarycode_boek(item['k_code'])
    return items


def list_librarycode(request, librarywild):
    template = loader.get_template('flac/librarycodes.html')
    items = get_full_items(librarywild)
    return HttpResponse(template.render(
        {
            'items': items,
            'page_title': 'LibrayCodes (' + librarywild + ')',
            'librarywild': librarywild
        }, request))


