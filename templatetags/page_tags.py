from django.template import Library
from ..services import menu_items

register = Library()


@register.inclusion_tag(
    'tagtemplates/navbar.html',
    takes_context=True
)
def navbar(context):
    request = context['request']
    context['menu'] = menu_items()
    context['menu_active'] = request.path
    return context


@register.inclusion_tag(
    'tagtemplates/menu_item.html',
    takes_context=True
)
def render_menu_item(context, url, label, badge=None):
    request = context['request']
    context['active'] = request.path.startswith(url)
    context['url'] = url
    context['label'] = label
    context['badge'] = badge
    return context
