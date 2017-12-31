from django.http import HttpResponse
from django.template import loader
from ..db import (get_librarycode_sonata, get_librarycode_boek,
                  get_librarycode_sonatas,
                  get_prev_librarycode, get_next_librarycode,
                  get_librarycode_explanation, get_librarycode,
                  get_librarycode_sonatas_range,
                  get_album_performers, settings)
import os


def one_librarycode_content(librarycode, wild):
    code = get_librarycode(librarycode)
    d = get_librarycode_explanation(wild[:-2])
    description = None
    if d and len(d):
        description = d[0]
    prev_id = get_prev_librarycode(librarycode, wild)
    next_id = get_next_librarycode(librarycode, wild)
    return {
        'pieces': get_pieces(librarycode),
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


def from_range(crange):
    w = crange.split('-')
    return w[0], w[1]


def get_pieces(code, instrument_id=0):
    pieces = get_librarycode_sonata(code, instrument_id)
    for piece in pieces:
        piece['performers'] = get_album_performers(piece['Album']['ID'])
    return pieces


def image_exists(k_code):
    image_path = settings.LIBRARYCODE_PATH + k_code + '.png'
    return os.path.exists(image_path)


def get_nummer(k_code):
    if '_' in k_code:
        return k_code.split('_')[1]
    return None


def get_level(k_code):
    if '_' in k_code:
        return 'part'
    else:
        return 'main'


def get_full_items(wild, instrument_id, crange):
    if crange:
        cmin, cmax = from_range(crange)
        items = get_librarycode_sonatas_range(wild, cmin, cmax)
    else:
        items = get_librarycode_sonatas(wild)
    for item in items:
        item['pieces'] = get_pieces(item['k_code'], instrument_id)
        item['pianoboeken'] = get_librarycode_boek(item['k_code'])
        item['cls_code_level'] = get_level(item['k_code'])
        item['has_image'] = image_exists(item['k_code'])
        item['nr'] = get_nummer(item['k_code'])
    return items


def list_content(code, instrument_id, crange=None):
    wild = code + ' %'
    items = get_full_items(wild, instrument_id, crange)
    description = get_librarycode_explanation(code)[0]
    if crange:
        description += ' - ' + crange + \
                       ' - ' + get_librarycode_explanation(code, crange)[0]
    return {
            'items': items,
            'page_title': description,
            'wild': wild,
            'lazy': False,
        }


def list_librarycoderange(request, code, crange, instrument_id=0):
    template = loader.get_template('flac/librarycodes.html')
    content = list_content(code, instrument_id, crange)
    return HttpResponse(template.render(content, request))


def list_librarycode(request, code, instrument_id=0):
    template = loader.get_template('flac/librarycodes.html')
    content = list_content(code, instrument_id)
    return HttpResponse(template.render(content, request))
