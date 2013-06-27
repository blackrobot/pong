from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import ConfirmationForm, MatchForm, SingleGameForm
from .models import Game


@login_required
@require_POST
def match_submit(request):
    form = MatchForm(request.POST, submitter=request.user)

    if form.is_valid():
        won, lost = form.save()
        messages.success(
            request,
            ("<strong>Updated!</strong> {} wins and {} losses have "
             "been submitted for approval!").format(won, lost)
        )
        return redirect('/')
    return render(request, 'games/match.error.html', {'match_form': form})


@login_required
@require_POST
def single_game_submit(request):
    form = SingleGameForm(request.POST, submitter=request.user)

    if form.is_valid():
        form.save()
        messages.success(
            request,
            "<strong>Updated!</strong> Your game has been submitted "
            "for approval!"
        )
        return redirect('/')
    return render(request, 'games/single-game.error.html', {'game_form': form})


@login_required
@require_POST
def submit_confirmation(request):
    """ Processes a game confirmation request. """
    form = ConfirmationForm(request.POST)

    if form.is_valid():
        accepted = form.save(request.user)
    else:
        accepted = False

    if accepted:
        messages.success(
            request,
            "<strong>Tyte!</strong> We've updated the rankings based "
            "on your input."
        )
    else:
        messages.error(
            request,
            "<strong>Oh no!</strong> We couldn't record your update. "
            "Try again?"
        )

    return redirect('games:game_confirm')


@login_required
def game_confirm(request):
    """ Show the user a table of unconfirmed games, and allow them to confirm
    or reject them.
    """
    user = request.user
    games = Game.objects.filter(
        confirmed=False,
    ).filter(
        Q(winner=user) | Q(loser=user)
    ).exclude(claimant=user).order_by('date_created')

    return render(request, 'games/confirm.html', {
        'games': games,
    })


def index(request):
    if request.user.is_authenticated:
        single_game_form = SingleGameForm(submitter=request.user)
        match_form = MatchForm(submitter=request.user)

    else:
        single_game_form = match_form = None

    return render(request, 'games/index.html', {
        'rankings': User.objects.order_by('-rating__exposure', 'first_name'),
        'single_game_form': single_game_form,
        'match_form': match_form,
    })
