from django.http import HttpResponse
from django.template import loader
from ..db import get_tags, get_tag, get_tag_albums


def tag(request, tag_id):
    template = loader.get_template('flac/tag.html')
    return HttpResponse(template.render(
        {
            'items': get_tag_albums(tag_id),
            "tag": get_tag(tag_id)
        }, request))


def tags(request):
    template = loader.get_template('flac/tags.html')
    return HttpResponse(template.render(
        {
            "tags": get_tags(),
        }, request))
