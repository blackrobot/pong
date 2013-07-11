from django import template

register = template.Library()


@register.inclusion_tag('include/active-link.txt', takes_context=True)
def active(context, url):
    path = context['request'].path

    if path == '/':
        return {'active': url == '/'}

    return {'active': url.startswith(path)}
