from django.http import HttpResponse
from django.template import loader
from ..db import (get_librarycode_sonata, get_librarycode_boek,
                  get_librarycode_sonatas,
                  get_prev_librarycode, get_next_librarycode,
                  get_librarycode_explanation, get_librarycode,
                  get_librarycode_sonatas_range)


def one_librarycode_content(librarycode, wild):
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
    content = one_librarycode_content(librarycode, code)
    return HttpResponse(template.render(content, request))


def from_range(range):
    w = range.split('-')
    return w[0], w[1]


def get_full_items(wild, instrument_id, range):
    if range:
        min, max = from_range(range)
        items = get_librarycode_sonatas_range(wild, min, max)
    else:
        items = get_librarycode_sonatas(wild)
    for item in items:
        item['pieces'] = get_librarycode_sonata(item['k_code'],instrument_id)
        item['pianoboeken'] = get_librarycode_boek(item['k_code'])
    return items


def list_content(code, instrument_id, range=None):
    wild = code + ' %'
    items = get_full_items(wild, instrument_id, range)
    description = get_librarycode_explanation(code)[0]
    if range:
        description += ' ' + range
    return {
            'items': items,
            'page_title': description,
            'wild': wild
        }


def list_librarycoderange(request, code, range, instrument_id=0):
    template = loader.get_template('flac/librarycodes.html')
    content = list_content(code, instrument_id, range)
    return HttpResponse(template.render(content, request))


def list_librarycode(request, code, instrument_id=0):
    template = loader.get_template('flac/librarycodes.html')
    content = list_content(code, instrument_id)
    return HttpResponse(template.render(content, request))


