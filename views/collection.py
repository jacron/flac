from django.http import HttpResponse
from django.template import loader
from ..db import (get_collections, )


def collections(request):
    template = loader.get_template('flac/collections.html')
    ccollections = get_collections()
    return HttpResponse(template.render(
        {
            'albums': ccollections
        }, request))


