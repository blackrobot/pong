from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string

from .models import Game


DEFAULT_CONTEXT = {
    'domain': Site.objects.get_current().domain,
}


def email_notification(subject_string, tmpl_path, tmpl_context, to_emails):
    tmpl_context.update(DEFAULT_CONTEXT)
    subject = "{}{}".format(
        settings.EMAIL_SUBJECT_PREFIX,
        subject_string.strip(),
    )
    body = render_to_string(tmpl_path, tmpl_context)

    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, to_emails,
              fail_silently=not settings.DEBUG)


def request_confirmation(user, submitter):
    """ This will email a link to the given user asking them to confirm game
    outcomes.
    """
    email_notification(
        "Games awaiting confirmation!",
        'games/email.confirmation.txt',
        {'user': user, 'submitter': submitter},
        [user.email],
    )


def notify_rejected(game):
    """ This will email the claimant of the game notifying them that the other
    user has rejected their account.
    """
    claimant = game.claimant
    context = {
        'user': claimant,
        'opponent': game.winner if game.winner != claimant else game.loser,
        'time': game.date_created,
    }
    email_notification(
        "Your game entry was denied!",
        'games/email.rejected.txt',
        context,
        [game.claimant.email],
    )


class ConfirmationForm(forms.Form):
    confirmed_choices = (
        ('yes', 'yes'),
        ('no', 'no'),
    )

    game_id = forms.IntegerField(widget=forms.HiddenInput())
    confirmed = forms.ChoiceField(choices=confirmed_choices,
                                  widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        game_id = kwargs.pop('game_id', None)
        super(ConfirmationForm, self).__init__(*args, **kwargs)
        if game_id:
            self.fields['game_id'].initial = game_id

    def save(self, user):
        try:
            game = Game.objects.filter(
                Q(winner=user) | Q(loser=user),
                confirmed=False,
            ).exclude(claimant=user).get(id=self.cleaned_data.get('game_id'))
        except Game.DoesNotExist:
            return False

        confirmed = self.cleaned_data.get('confirmed', None)

        if confirmed is None:
            return False, None

        yes = confirmed == 'yes'

        if yes:
            game.confirmed = True
            game.save()

        else:
            notify_rejected(game)
            game.delete()

        return True, yes


class MatchForm(forms.Form):
    games_won = forms.IntegerField(initial=0, min_value=0, max_value=3)
    games_lost = forms.IntegerField(initial=0, min_value=0, max_value=3)

    def __init__(self, *args, **kwargs):
        self.submitter = submitter = kwargs.pop('submitter')
        opponents = (User.objects.exclude(pk=submitter.pk)
                     .order_by('first_name', 'last_name'))
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['opponent'] = forms.ChoiceField(
            choices=((o.pk, o.get_full_name()) for o in opponents),
            label="Who was your opponent?",
        )

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        won = int(data.get('games_won', 0))
        lost = int(data.get('games_lost', 0))

        acceptable = (
            (0 <= won < 3) and
            (0 <= lost < 3) and
            2 <= (won + lost) <= 3
        )

        if not acceptable:
            raise forms.ValidationError(
                "Invalid combination of won/lost games.")

        return data

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        opponent = User.objects.get(pk=self.cleaned_data.get('opponent'))
        data = self.cleaned_data
        won, lost = int(data.get('games_won')), int(data.get('games_lost'))

        for i in range(won):
            Game.objects.create(
                winner=self.submitter,
                loser=opponent,
                claimant=self.submitter,
            )

        for i in range(lost):
            Game.objects.create(
                winner=opponent,
                loser=self.submitter,
                claimant=self.submitter,
            )

        request_confirmation(opponent, self.submitter)

        return won, lost


class SingleGameForm(forms.Form):
    WIN_LOSE_CHOICES = (('lose', 'I Lost'), ('win', 'I Won'))
    win_lose = forms.ChoiceField(choices=WIN_LOSE_CHOICES,
                                 label="Did you win or lose?")

    def __init__(self, *args, **kwargs):
        self.submitter = submitter = kwargs.pop('submitter')
        opponents = (User.objects.exclude(pk=submitter.pk)
                     .order_by('first_name', 'last_name'))
        super(SingleGameForm, self).__init__(*args, **kwargs)
        self.fields['opponent'] = forms.ChoiceField(
            choices=((o.pk, o.get_full_name()) for o in opponents),
            label="Who was your opponent?",
        )

    def save(self, *args, **kwargs):
        opponent = User.objects.get(pk=self.cleaned_data.get('opponent'))

        if self.cleaned_data.get('win_lose') == 'lose':
            winner, loser = opponent, self.submitter
        else:
            winner, loser = self.submitter, opponent

        Game.objects.create(
            winner=winner,
            loser=loser,
            claimant=self.submitter,
        )

        request_confirmation(opponent, self.submitter)
