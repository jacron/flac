from django.http import HttpResponse
from django.template import loader

from flac.services.clipboard import save_cb_image, save_cb_images
from ..db import (get_scarlatti_k_pieces, get_scarlatti, get_setting,
                  toggle_setting, get_widow_albums, get_apeflac_albums,
                  get_bach_k_pieces, get_codes, get_pathdoubles_albums)


def extra_view(request, albums=None):
    template = loader.get_template('flac/extra.html')
    rc = get_setting('read_cuesheet')
    sp = get_setting('show_proposals')
    codes = get_codes()
    return HttpResponse(template.render(
        {
            'read_cuesheet': rc['VALUE'],
            'show_proposals': sp['VALUE'],
            'albums': albums,
            'codes': codes,
        }, request))


def extra(request):
    return extra_view(request)


def list_scarlatti(request):
    template = loader.get_template('flac/librarycode_pieces.html')
    return HttpResponse(template.render(
        {
            'items': get_scarlatti_k_pieces(),
            'scarlatti': get_scarlatti(),
            'page_title': 'Scarlatti Sonaten (Kirkpatrick nummering)',
        }, request))


def list_bach(request):
    template = loader.get_template('flac/librarycode_pieces.html')
    return HttpResponse(template.render(
        {
            'items': get_bach_k_pieces(),
            'page_title': 'Bach Goldberg',
        }, request))


# def missing_score(request):
#     template = loader.get_template('flac/missing.html')
#     missing = get_missing_score()
#     return HttpResponse(template.render(
#         {'items': missing}, request
#     ))

def cmd(request, cmd_code):
    if cmd_code == 'scarlatti':
        return list_scarlatti(request)
    if cmd_code == 'bach':
        return list_bach(request)
    if cmd_code == 'cue':
        toggle_setting('read_cuesheet')
        return extra_view(request)
    # if cmd_code == 'proposals':
    #     toggle_setting('show_proposals')
    #     return extra_view(request)
    if cmd_code == 'folder':
        save_cb_image('folder')
        return extra_view(request)
    if cmd_code == 'back':
        save_cb_image('back')
        return extra_view(request)
    if cmd_code == 'folderback':
        save_cb_images('folder', 'back')
        return extra_view(request)
    if cmd_code == 'widows':
        return extra_view(request, get_widow_albums())
    if cmd_code == 'apeflac':
        return extra_view(request, get_apeflac_albums())
    # if cmd_code == 'missingscore':
    #     return missing_score(request)
    if cmd_code == 'pathdoubles':
        return extra_view(request, get_pathdoubles_albums())
    return extra_view(request)
