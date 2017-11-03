from django.template import Library

from flac.db import get_album, get_album_albums, get_mother_title, get_album_componisten, get_album_performers, \
    get_album_instruments, get_album_tags
from flac.views import organize_pieces, get_proposals, get_artists
from . import MENU_ITEMS


register = Library()


@register.inclusion_tag(
    'tagtemplates/navbar.html',
    takes_context=True
)
def navbar(context):
    request = context['request']
    context['menu'] = MENU_ITEMS
    context['menu_active'] = request.path
    return context


@register.inclusion_tag(
    'tagtemplates/albumlist.html',
    takes_context=True
)
def albumlist(context, albums):
    context['albums'] = albums
    return context


@register.inclusion_tag(
    'tagtemplates/componistenlist.html',
    takes_context=True
)
def componistenlist(context, items):
    context['items'] = items
    return context


@register.inclusion_tag(
    'tagtemplates/performerslist.html',
    takes_context=True
)
def performerslist(context, items):
    context['items'] = items
    return context


#     {% editalbum 'select-performer' 'add-performer' album.ID performers %}

@register.inclusion_tag(
    'tagtemplates/editalbum.html',
)
def editalbum(select, add, albumid, options):
    return dict(select=select, add=add, albumid=albumid, options=options)


@register.inclusion_tag(
    'tagtemplates/album_controls.html',
)
def album_controls(album_id):
    return dict(album_id=album_id)


@register.inclusion_tag(
    'tagtemplates/albumdetails.html',
)
def albumdetails(album_id):
    mother_title = None
    cuesheets, pieces, proposals, artists = [], [], [], []
    album_o = get_album(album_id)
    if album_o['AlbumID']:
        mother_title = get_mother_title(album_o['AlbumID'])
        cuesheets, pieces = organize_pieces(album_id, album_o['Path'])
        proposals = get_proposals(cuesheets, album_o['Title'])
        artists = get_artists(cuesheets, album_o['Title'])
    return {
        'albumid': album_id,
        'items': pieces,
        'albums': get_album_albums(album_id),
        'album': album_o,
        'mother_title': mother_title,
        'album_componisten': get_album_componisten(album_id),
        'album_performers': get_album_performers(album_id),
        'album_instrument': get_album_instruments(album_id),
        'cuesheet_output': cuesheets,
        'album_tags': get_album_tags(album_id),
        'proposals': proposals,
        'artists': artists,
    }


