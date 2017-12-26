from django.http import HttpResponse
from django.template import loader
from ..db import (get_librarycode_sonata, get_librarycode_boek,
                  get_librarycode_sonatas,
                  get_prev_librarycode, get_next_librarycode)


def librarycode_content(librarycode):
    # prev_id = get_prev_librarycode(librarycode)
    # next_id = get_next_librarycode(librarycode)
    return {
        'pieces': get_librarycode_sonata(librarycode),
        'boeken': get_librarycode_boek(librarycode),
        'librarycode': librarycode,
        'page_title': 'Scarlatti Sonaten ({})'.format(librarycode),
        # 'prev_id': prev_id,
        # 'next_id': next_id,
    }


def one_librarycode(request, librarycode):
    template = loader.get_template('flac/scarlatti_kcode.html')
    content = librarycode_content(librarycode)
    return HttpResponse(template.render(content, request))


def list_librarycode(request, librarycode):
    template = loader.get_template('flac/scarlatti_kk.html')
    return HttpResponse(template.render(
        {
            'items': get_librarycode_sonatas(librarycode),
            'page_title': 'List (' + librarycode + ')',
        }, request))


