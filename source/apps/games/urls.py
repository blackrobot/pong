from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'source.apps.games.views',

    # Game form submissions
    url(r"^match/submit/$", 'match_submit', name="match_submit"),
    url(r"^game/submit/$", 'single_game_submit', name="single_submit"),

    # Login
    url(r"^login/$", 'user_login', name="login"),

    # Rankings
    url(r"^$", 'index', name="index"),
)
