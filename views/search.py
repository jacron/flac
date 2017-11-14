from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from flac.db import get_albums_by_title, get_general_search
from flac.forms import SearchForm


def searchq(request, query):
    template = loader.get_template('flac/searchq.html')
    return HttpResponse(template.render(
        {
            'query': query,
            'albums': get_albums_by_title(query)
        }, request))


def search(request):
    # template = loader.get_template('flac/search.html')
    # return HttpResponse(template.render(
    #     {
    #     }, request))
    form = SearchForm
    return render(request, 'flac/search.html', {'form': form})

