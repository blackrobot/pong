import json

from django import template
from django.db.models import Q

from source.apps.games.models import Game


register = template.Library()


@register.filter
def confirmed_count(games):
    """ Returns the count of confirmed games. """
    return games.filter(confirmed=True).count()


@register.filter
def ratio(wins, losses):
    """ Returns the ratio of wins to total games. """
    total = float(wins + losses)
    if total > 0:
        return int(round(wins / total * 100.0, 0))
    return None


@register.filter
def record(user, opponent):
    wins = Game.objects.filter(confirmed=True).filter(
        (Q(winner=user) & Q(loser=opponent)) |
        (Q(loser=user) & Q(winner=opponent))
    ).order_by('date_created').values_list('winner__id', flat=True)[:20]
    return json.dumps([1 if w == user.id else -1 for w in wins])
