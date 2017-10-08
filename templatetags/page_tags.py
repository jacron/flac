from django.template import Library

register = Library()


@register.inclusion_tag(
    '/tagtemplates/hyperlink.html',
    takes_context=True
)
def hyperlink(context):
    return context

