from django.http import HttpResponse
from django.template import loader
from ..db import get_instrument, get_instrument_albums, get_instruments, get_instrument_albums_search
from django.conf import settings


def instrument_search(request, instrument_id, query):
    template = loader.get_template('flac/instrument.html')
    context = {
        'items': get_instrument_albums_search(instrument_id, query),
        'instrument': get_instrument(instrument_id),
        'instruments_path': settings.INSTRUMENTS_PATH,
        'instrument_id': instrument_id,
        'query': query,
    }
    return HttpResponse(template.render(context, request))


def instrument(request, instrument_id):
    template = loader.get_template('flac/instrument.html')
    context = {
        'items': get_instrument_albums(instrument_id),
        'instrument': get_instrument(instrument_id),
        'instruments_path': settings.INSTRUMENTS_PATH,
        'instrument_id': instrument_id,
    }
    return HttpResponse(template.render(context, request))


def instrumenten(request):
    context = {
        'items': get_instruments(),
        'instruments_path': settings.INSTRUMENTS_PATH
    }
    template = loader.get_template('flac/instrumenten.html')
    return HttpResponse(template.render(context, request))
