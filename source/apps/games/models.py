from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

import trueskill
from picklefield.fields import PickledObjectField

from source.apps.abstract.models import CommonModel, QuerySet


_env = trueskill.TrueSkill(draw_probability=0.00)
_env.make_as_global()


class Rating(CommonModel):
    user = models.OneToOneField(User)
    ts_rating = PickledObjectField(default=trueskill.Rating, editable=False)
    exposure = models.FloatField(default=0, editable=False)

    class Meta:
        ordering = ('-exposure',)

    def save(self, *args, **kwargs):
        self.exposure = trueskill.expose(self.ts_rating)
        super(Rating, self).save(*args, **kwargs)

    def update_rating(self, outcome):
        self.ts_rating = outcome
        self.save()


@receiver(post_save, sender=User)
def user_post_save(sender, instance, signal, created, **kwargs):
    if created:
        Rating.objects.get_or_create(user=instance)


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    instance.rating.delete()


class GameQuerySet(QuerySet):
    def confirmed(self):
        return self.filter(confirmed=True)

    def played_by(self, *players):
        return self.filter(
            *[Q(winner=player) | Q(loser=player) for player in players]
        )

    def awaiting_confirmation(self, player):
        return self.played_by(player).filter(
            confirmed=False,
            rejected=False,
            claimant=player,
        ).order_by('date_created')

    def unconfirmed_games(self, player):
        return self.played_by(player).filter(
            confirmed=False,
            rejected=False,
        ).exclude(claimant=player).order_by('date_created')


class Game(CommonModel):
    winner = models.ForeignKey(User, related_name='wins')
    loser = models.ForeignKey(User, related_name='losses')

    claimant = models.ForeignKey(User, related_name='claims')
    confirmed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    objects = GameQuerySet.as_manager()

    class Meta:
        ordering = ['date_created']

    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)

        if self.confirmed:
            self.calculate_ratings()

    def clean(self):
        if self.confirmed and self.rejected:
            raise ValidationError("Game cannot be confirmed and rejected!")

    def calculate_ratings(self):
        outcomes = trueskill.rate_1vs1(
            self.winner.rating.ts_rating,
            self.loser.rating.ts_rating,
        )
        self.winner.rating.update_rating(outcomes[0])
        self.loser.rating.update_rating(outcomes[1])

    def opponent(self, user):
        if self.winner == user:
            return self.loser
        return self.winner

    @property
    def form(self):
        from .forms import ConfirmationForm
        return ConfirmationForm(game_id=self.id)
