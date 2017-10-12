from django.template import Library

register = Library()


@register.inclusion_tag(
    'tagtemplates/navbar.html',
    takes_context=True
)
def navbar(context, menu):
    context['menu'] = menu
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
