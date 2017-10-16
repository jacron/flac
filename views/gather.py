from django.http import HttpResponse
from django.template import loader
from ..db import get_gatherers


def gather(request):
    template = loader.get_template('flac/gatherers.html')
    return HttpResponse(template.render(
        {
            "albums": get_gatherers()
        }, request))


