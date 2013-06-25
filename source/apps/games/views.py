from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import MatchForm, SingleGameForm


@require_POST
def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user is not None and user.is_active:
        login(request, user)
        return redirect('/')

    messages.error(request,
                   "<strong>Nope!</strong> We were unable to log you in.")

    return redirect('/?fail')


@login_required
@require_POST
def match_submit(request):
    form = MatchForm(request.POST, submitter=request.user)

    if form.is_valid():
        won, lost = form.save()
        messages.success(
            request,
            ("<strong>Updated!</strong> {} wins and {} losses have "
             "been recorded.").format(won, lost)
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
            request, "<strong>Updated!</strong> Your game has been recorded!")
        return redirect('/')
    return render(request, 'games/single-game.error.html', {'game_form': form})


def index(request):
    if request.user.is_authenticated:
        single_game_form = SingleGameForm(submitter=request.user)
        match_form = MatchForm(submitter=request.user)

    else:
        single_game_form = match_form = None

    return render(request, 'games/index.html', {
        'rankings': User.objects.order_by('-rating__mu'),
        'single_game_form': single_game_form,
        'match_form': match_form,
    })
