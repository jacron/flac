from django.http import HttpResponse
from django.template import loader
from ..db import (get_scarlatti_k_pieces, get_scarlatti, get_setting,
                  toggle_setting, )


def extra_view(request):
    template = loader.get_template('flac/extra.html')
    rc = get_setting('read_cuesheet')
    return HttpResponse(template.render(
        {
            'read_cuesheet': rc['VALUE']
        }, request))


def extra(request):
    return extra_view(request)


def list_scarlatti(request):
    template = loader.get_template('flac/scarlatti_k.html')
    return HttpResponse(template.render(
        {
            'items': get_scarlatti_k_pieces(),
            'scarlatti': get_scarlatti(),
            'page_title': 'Scarlatti Sonaten (Kirkpatrick nummering)',
        }, request))


def cmd(request, cmd_code):
    if cmd_code == 'k':
        return list_scarlatti(request)
    if cmd_code == 'cue':
        toggle_setting('read_cuesheet')
        return extra_view(request)

