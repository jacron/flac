from django.http import HttpResponse
from django.template import loader
from ..db import get_scarlatti_k_pieces

def extra(request):
    template = loader.get_template('flac/extra.html')
    return HttpResponse(template.render(
        {
        }, request))


def list_scarlatti(request):
    template = loader.get_template('flac/scarlatti_k.html')
    return HttpResponse(template.render(
        {
            'items': get_scarlatti_k_pieces(),
        }, request))


def cmd(request, cmd_code):
    if cmd_code == 'k':
        return list_scarlatti(request)
