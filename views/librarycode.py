from django.http import HttpResponse
from django.template import loader
from ..db import (get_librarycode_sonata, get_librarycode_boek,
                  get_librarycode_sonatas,
                  get_prev_librarycode, get_next_librarycode,
                  get_librarycode_explanation, get_librarycode)


def librarycode_content(librarycode, wild):
    code = get_librarycode(librarycode)
    d = get_librarycode_explanation(wild[:-2])
    description = None
    if d and len(d):
        description = d[0]
    prev_id = get_prev_librarycode(librarycode, wild)
    next_id = get_next_librarycode(librarycode, wild)
    return {
        'pieces': get_librarycode_sonata(librarycode),
        'boeken': get_librarycode_boek(librarycode),
        'librarycode': librarycode,
        'prev_id': prev_id,
        'next_id': next_id,
        'code': code,
        'wild': wild,
        'description': description,
    }


def one_librarycode(request, librarycode, code='dummy'):
    template = loader.get_template('flac/librarycode.html')
    content = librarycode_content(librarycode, code)
    return HttpResponse(template.render(content, request))


def get_full_items(wild, instrument_id):
    items = get_librarycode_sonatas(wild)
    for item in items:
        item['pieces'] = get_librarycode_sonata(item['k_code'],instrument_id)
        item['pianoboeken'] = get_librarycode_boek(item['k_code'])
    return items


def list_librarycode(request, code, instrument_id=0):
    wild = code + ' %'
    template = loader.get_template('flac/librarycodes.html')
    items = get_full_items(wild, instrument_id)
    description = get_librarycode_explanation(code)[0]
    return HttpResponse(template.render(
        {
            'items': items,
            'page_title': description,
            'wild': wild
        }, request))


