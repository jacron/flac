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
    'tagtemplates/componistenlist.html',
    takes_context=True
)
def componistenlist(context, items):
    context['items'] = items
    return context


@register.inclusion_tag(
    'tagtemplates/performerslist.html',
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