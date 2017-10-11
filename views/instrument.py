from django.http import HttpResponse
from django.template import loader
from ..db import get_instrument, get_instrument_albums, get_instruments


def instrument(request, instrument_id):
    template = loader.get_template('flac/instrument.html')
    context = {
        'items': get_instrument_albums(instrument_id),
        'instrument': get_instrument(instrument_id),
    }
    return HttpResponse(template.render(context, request))


def instrumenten(request):
    context = {'items': get_instruments()}
    template = loader.get_template('flac/instrumenten.html')
    return HttpResponse(template.render(context, request))
