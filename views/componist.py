from django.http import HttpResponse
from django.template import loader
from ..db import get_componist_albums, get_componisten, get_componist


def componist(request, componist_id):
    template = loader.get_template('flac/componist.html')
    context = {
        'items': get_componist_albums(componist_id),
        'componist': get_componist(componist_id),
    }
    return HttpResponse(template.render(context, request))


def componisten(request):
    template = loader.get_template('flac/componisten.html')
    context = {
        'items': get_componisten(),
    }
    return HttpResponse(template.render(context, request))
