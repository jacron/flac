from django.http import HttpResponse
from django.template import loader
from ..db import get_performers, get_performer_albums, get_performer


def performer(request, performer_id):
    template = loader.get_template('flac/performer.html')
    context = {
        'items': get_performer_albums(performer_id),
        'performer': get_performer(performer_id)
    }
    return HttpResponse(template.render(context, request))


def performers(request):
    template = loader.get_template('flac/performers.html')
    context = {'performers': get_performers()}
    return HttpResponse(template.render(context, request))
