from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'source.apps.games.views',

    # Game form submissions
    url(r"^match/submit/$", 'match_submit', name="match_submit"),
    url(r"^game/submit/$", 'single_game_submit', name="single_submit"),

    # Confirmation form submissions
    url(r"^game/confirm/$", 'game_confirm', name="game_confirm"),
    url(r"^game/confirm/submit/$", 'submit_confirmation',
        name="submit_confirmation"),

    # Awaiting confirmation
    url(r"^game/unconfirmed/$", 'awaiting_confirmation',
        name="awaiting_confirmation"),

    # Rankings
    url(r"^$", 'index', name="index"),
)
