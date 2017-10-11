from django.http import HttpResponse
from django.template import loader
from ..db import get_performers, get_performer_albums


def performer(request, performer_id):
    template = loader.get_template('flac/performer.html')
    items = get_performer_albums(performer_id)
    context = {
        'items': items,
    }
    return HttpResponse(template.render(context, request))


def performers(request):
    template = loader.get_template('flac/performers.html')
    context = {'performers': get_performers()}
    return HttpResponse(template.render(context, request))
