from django import forms
from django.contrib.auth.models import User

from .models import Game


class GameForm(forms.Form):
    win_lose = forms.ChoiceField(choices=((0, 'I Lost'), (1, 'I Won')),
                                 label="Did you win or lose?")

    def __init__(self, *args, **kwargs):
        self.submitter = submitter = kwargs.pop('submitter')
        opponents = User.objects.exclude(pk=submitter.pk)
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['opponent'] = forms.ChoiceField(
            choices=((o.pk, o.get_full_name()) for o in opponents),
            label="Who was your opponent?",
        )

    def save(self, *args, **kwargs):
        opponent = User.objects.get(pk=self.cleaned_data.get('opponent'))
        if self.cleaned_data.get('win_lose') is 0:
            winner, loser = opponent, self.submitter
        else:
            winner, loser = self.submitter, opponent
        Game.objects.create(winner=winner, loser=loser)
