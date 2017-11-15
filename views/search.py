from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from flac.db import get_albums_by_title, get_general_search
from flac.forms import SearchForm


def searchresponse(context, request):
    template = loader.get_template('flac/searchq.html')
    return HttpResponse(template.render(context, request))


def searchq(request, query):
    context = {
            'query': query,
            'albums': get_albums_by_title(query)
        }
    return searchresponse(context, request)


def search(request):
    return searchresponse({}, request)

