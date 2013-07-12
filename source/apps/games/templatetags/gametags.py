from django import template

from source.apps.games.models import Game

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_opponent(context, game):
    user = context['request'].user
    if user == game.winner:
        return game.loser
    return game.winner


@register.inclusion_tag('games/unconfirmed.html')
def unconfirmed_games(player):
    return {
        'unconfirmed_count': Game.objects.unconfirmed_games(player).count(),
    }
