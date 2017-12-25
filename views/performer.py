from django.http import HttpResponse
from django.template import loader

from flac import settings
from flac.services import alfabet
from ..db import get_performers, get_performer_albums, get_performer, delete_performer, get_performer_path

import os


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


def has_image(performer_id):
    performer_path = get_performer_path(performer_id)
    if performer_path:
        image_path = performer_path + settings.PERSON_FILE
        return os.path.exists(image_path)
    return False


def performers(request):
    template = loader.get_template('flac/performers.html')
    performers = get_performers()
    for performer in performers:
        performer['has_image'] = has_image(performer['ID'])
    context = {'performers': performers, 'letters': alfabet()}
    return HttpResponse(template.render(context, request))
