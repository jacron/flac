import json
import os

from django.http import HttpResponse


def ajax(request):
    if request.POST:
        args = request.POST['args']
        os.system('open -a "/Applications/Media Center 21.app" "' + args + '"')
        return HttpResponse('Playing: ' + args)
    else:
        return HttpResponse('Not a post request')

