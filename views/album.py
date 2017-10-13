from cueparser import CueSheet
from django.http import HttpResponse
from django.template import loader
from ..db import get_albums, get_album, get_pieces, get_componist, get_album_albums, get_album_performers


def get_title(data):
    for line in data.split('\n'):
        if line[:5] == 'TITLE':
            return line[5:]


def album(request, album_id):
    template = loader.get_template('flac/album.html')
    album_o = get_album(album_id)
    # cuesheet = CueSheet()
    # header = u'%performer% - %title%\n%file%\n%tracks%'
    # track = u'%performer% - %title%'
    # cuesheet.setOutputFormat(header, track)
    items = get_pieces(album_id)
    cuesheets = []
    for item in items:
        file = item[0]
        # print(file)
        if file:
            extension = file.split('.')[-1]
            if extension == 'cue':
                path = '{}/{}'.format(album_o['Path'], file)
                # print(path)
                with open(path, 'r') as f:
                    data = f.read()
                    cuesheets.append({
                        'Title': get_title(data),
                        'ID': item[1]
                    })
                    # item['Title'] = get_title(data)
                    # print(data)
                    # if data:
                    # cuesheet.setData(f.read())
                        # cuesheets.append(data)
    # cuesheet.parse()

    context = {
        'items': items,
        'albums': get_album_albums(album_id),
        'album': album_o,
        'componist': get_componist(album_o['ComponistID']),
        'performers': get_album_performers(album_id),
        'cuesheet_output': cuesheets
    }
    return HttpResponse(template.render(context, request))


def albums(request):
    template = loader.get_template('flac/albums.html')
    return HttpResponse(template.render(
        {
            'albums': get_albums(),
        }, request))
