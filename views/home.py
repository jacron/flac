from django.http import HttpResponse
from django.template import loader


def home(request):
    template = loader.get_template('flac/home.html')
    return HttpResponse(template.render(
        {
        }, request))
