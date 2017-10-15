from django.http import HttpResponse
from django.template import loader


def gather(request):
    template = loader.get_template('flac/gather.html')
    return HttpResponse(template.render(
        {
        }, request))
