import os
from django.http import HttpResponse
from ..db import get_album
from django.conf import settings


def play(args):
    uargs = args.encode('utf-8')
    os.system('open -a "{}" "{}"'.format(settings.MEDIA_PLAYER, uargs))


def openfinder(args):
    album = get_album(args)
    os.system('open "' + album['Path'] + '"')


def ajax(request):
    if request.POST:
        cmd = request.POST['cmd']
        msg = 'Uitgevoerd cmd: ' + cmd
        if cmd == 'play':
            play(request.POST['arg'])
        if cmd == 'openfinder':
            openfinder(request.POST['arg'])
    else:
        msg = 'Dit is geen POST request'
    print(msg)
    return HttpResponse(msg)
