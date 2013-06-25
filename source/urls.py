from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from source.utils.tools import local_serve_urlpatterns


admin.autodiscover()

urlpatterns = patterns(
    '',

    # Django Admin
    url(r"^{}/".format(settings.ADMIN_NAMESPACE), include(admin.site.urls)),

    # Games gets the root
    url(r"^", include('source.apps.games.urls',
                      namespace="games", app_name="games")),
)

if getattr(settings, "LOCAL_SERVE", False):
    urlpatterns = local_serve_urlpatterns() + urlpatterns
