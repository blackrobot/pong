from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from source.utils.tools import local_serve_urlpatterns


admin.autodiscover()

urlpatterns = patterns(
    '',

    # Django Admin
    url(r"^%s/" % settings.ADMIN_NAMESPACE, include(admin.site.urls)),

    # Game Submit
    url(r"^submit-game/$", 'source.apps.games.views.submit', name="submit"),

    # User Login
    url(r"^login/$", 'source.apps.games.views.user_login', name="login"),

    # Index
    url(r"^$", 'source.apps.games.views.index', name="index"),
)

if getattr(settings, "LOCAL_SERVE", False):
    urlpatterns = local_serve_urlpatterns() + urlpatterns
