from django.http import HttpResponse
from django.template import loader

from flac.services import save_cb_image, save_cb_images
from ..db import (get_scarlatti_k_pieces, get_scarlatti, get_setting,
                  toggle_setting, get_widow_albums, get_apeflac_albums, get_scarlatti_k_sonatas, get_scarlatti_k_sonata,
                  get_scarlatti_k_boeken)


def extra_view(request, albums=None):
    template = loader.get_template('flac/extra.html')
    rc = get_setting('read_cuesheet')
    sp = get_setting('show_proposals')
    return HttpResponse(template.render(
        {
            'read_cuesheet': rc['VALUE'],
            'show_proposals': sp['VALUE'],
            'albums': albums,
        }, request))


def extra(request):
    return extra_view(request)


def list_scarlatti(request):
    template = loader.get_template('flac/scarlatti_k.html')
    return HttpResponse(template.render(
        {
            'items': get_scarlatti_k_pieces(),
            'scarlatti': get_scarlatti(),
            'page_title': 'Scarlatti Sonaten (Kirkpatrick nummering)',
        }, request))


def list_scarlatti_sonatas(request):
    template = loader.get_template('flac/scarlatti_kk.html')
    return HttpResponse(template.render(
        {
            'items': get_scarlatti_k_sonatas(),
            'scarlatti': get_scarlatti(),
            'page_title': 'Scarlatti Sonaten (Kirkpatrick nummering)',
        }, request))


def k_code(request, k_code):
    template = loader.get_template('flac/scarlatti_kcode.html')
    return HttpResponse(template.render(
        {
            'pieces': get_scarlatti_k_sonata(k_code),
            'boeken': get_scarlatti_k_boeken(k_code),
            'scarlatti': get_scarlatti(),
            'librarycode': k_code,
            'page_title': 'Scarlatti Sonaten ({})'.format(k_code),
        }, request))


def cmd(request, cmd_code):
    if cmd_code == 'k':
        return list_scarlatti(request)
    if cmd_code == 'kk':
        return list_scarlatti_sonatas(request)
    if cmd_code == 'cue':
        toggle_setting('read_cuesheet')
        return extra_view(request)
    if cmd_code == 'proposals':
        toggle_setting('show_proposals')
        return extra_view(request)
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
    return extra_view(request)




