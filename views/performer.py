from django.http import HttpResponse
from django.template import loader

from flac.services import alfabet
from ..db import get_performers, get_performer_albums, get_performer, delete_performer


def performer_delete(request, performer_id):
    performer = get_performer(performer_id)
    delete_performer(performer_id)
    template = loader.get_template('flac/performer_deleted.html')
    return HttpResponse(template.render({'performer': performer}, request))


def performer(request, performer_id):
    template = loader.get_template('flac/performer.html')
    context = {
        'items': get_performer_albums(performer_id),
        'performer': get_performer(performer_id)
    }
    return HttpResponse(template.render(context, request))


def performers(request):
    template = loader.get_template('flac/performers.html')
    context = {'performers': get_performers(), 'letters': alfabet()}
    return HttpResponse(template.render(context, request))
