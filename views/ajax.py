import os

from django.http import HttpResponse
from .. import services
from ..db import get_album

player = '/Applications/Media Center 21.app'


def play(args):
    uargs = args.encode('utf-8')
    os.system('open -a "{}" "{}"'.format(player, uargs))


def openfinder(args):
    album = get_album(args)
    path = services.directory(album['Path'])
    os.system('open "' + path + '"')


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
