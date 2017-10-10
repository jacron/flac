import sqlite3

from django.http import HttpResponse
from django.template import loader
from ..db import get_albums, get_componisten


def home(request):
    template = loader.get_template('flac/home.html')
    return HttpResponse(template.render(
        {
            'albums': get_albums(),
            'componisten': get_componisten(),
         }, request))
