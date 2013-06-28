from django import template


register = template.Library()


@register.filter
def confirmed_count(games):
    """ Returns the count of confirmed games. """
    return games.filter(confirmed=True).count()
