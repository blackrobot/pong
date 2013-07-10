from django import template

from source.apps.games.models import Game

register = template.Library()


@register.inclusion_tag('games/unconfirmed.html')
def unconfirmed_games(player):
    return {
        'unconfirmed_count': Game.objects.unconfirmed_games(player).count(),
    }
