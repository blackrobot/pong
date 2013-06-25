from django import forms
from django.contrib.auth.models import User

from .models import Game


class MatchForm(forms.Form):
    games_won = forms.IntegerField(initial=0, min_value=0, max_value=3)
    games_lost = forms.IntegerField(initial=0, min_value=0, max_value=3)

    def __init__(self, *args, **kwargs):
        self.submitter = submitter = kwargs.pop('submitter')
        opponents = User.objects.exclude(pk=submitter.pk)
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
            Game.objects.create(winner=self.submitter, loser=opponent)

        for i in range(lost):
            Game.objects.create(winner=opponent, loser=self.submitter)

        return won, lost


class SingleGameForm(forms.Form):
    WIN_LOSE_CHOICES = (('lose', 'I Lost'), ('win', 'I Won'))
    win_lose = forms.ChoiceField(choices=WIN_LOSE_CHOICES,
                                 label="Did you win or lose?")

    def __init__(self, *args, **kwargs):
        self.submitter = submitter = kwargs.pop('submitter')
        opponents = User.objects.exclude(pk=submitter.pk)
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

        Game.objects.create(winner=winner, loser=loser)
