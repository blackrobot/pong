from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import GameForm


@require_POST
def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user is not None and user.is_active:
        login(request, user)
        return redirect('/')
    return redirect('/?fail')


@require_POST
def submit(request):
    form = GameForm(request.POST, submitter=request.user)

    if form.is_valid():
        form.save()
        return redirect('/')
    return redirect('/?fail')


def index(request):
    if request.user.is_authenticated:
        game_form = GameForm(submitter=request.user)
    else:
        game_form = None

    return render(request, 'index.html', {
        'rankings': User.objects.order_by('-rating__mu'),
        'game_form': game_form,
        'login_fail': request.GET.get('fail'),
    })
