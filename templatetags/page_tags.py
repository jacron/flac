from django.template import Library
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
    'tagtemplates/cuesheetlist.html',
)
def cuesheetlist(cuesheets):
    return dict(cuesheets=cuesheets)


@register.inclusion_tag(
    'tagtemplates/pieceslist.html',
)
def pieceslist(items):
    return dict(items=items)


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
