from django.template import Library
from . import MENU_ITEMS
from flac.services import alfabet as alph


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
def albumlist(context, albums, list_id=None, list_name=None):
    context['albums'] = albums
    context['list_id'] = list_id
    context['list_name'] = list_name
    return context


@register.inclusion_tag(
    'tagtemplates/cuesheetlist.html',
)
def cuesheetlist(cuesheets, valid):
    return dict(cuesheets=cuesheets, valid=valid)


@register.inclusion_tag(
    'tagtemplates/pieceslist.html',
)
def pieceslist(pieces):
    return dict(pieces=pieces)


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


@register.inclusion_tag(
    'tagtemplates/editalbum.html',
)
def editalbum(select, add, albumid, options):
    return dict(select=select, add=add, albumid=albumid, options=options)


@register.inclusion_tag(
    'tagtemplates/proposallist.html',
)
def proposallist(proposals, artists):
    return dict(proposals=proposals,artists=artists)


@register.inclusion_tag(
    'tagtemplates/album_controls.html',
)
def album_controls(album_id):
    return dict(album_id=album_id)


@register.inclusion_tag(
    'tagtemplates/persons_list.html',
)
def persons_list(persons, url, type):
    return dict(persons=persons, person_url=url, type=type)


@register.inclusion_tag(
    'tagtemplates/alfabet.html',
)
def alfabet():
    return dict(letters=alph())


@register.filter( name='unescape' )
def unescape(val):
    unescape.is_safe = True
    if isinstance(val, str):
        return val.encode( 'string-escape' )
    else:
        return val


