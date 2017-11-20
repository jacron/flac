from django.http import HttpResponse
from django.template import loader


def uploadalbum(request):
    template = loader.get_template('flac/upload.html')
    return HttpResponse(template.render(
        {
        }, request))
