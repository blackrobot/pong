from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from source.utils.tools import local_serve_urlpatterns


admin.autodiscover()

urlpatterns = patterns(
    '',

    # Django Admin
    url(r"^{}/".format(settings.ADMIN_NAMESPACE), include(admin.site.urls)),

    # Auth
    url(r"^user/login/$", 'django.contrib.auth.views.login', name="login"),
    url(r"^user/logout/$", 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name="logout"),
    url(r"^user/change-password/$",
        'django.contrib.auth.views.password_change', name="password_change"),
    url(r"^user/change-password/done/$",
        'django.contrib.auth.views.password_change_done',
        name="password_change_done"),

    # Games gets the root
    url(r"^", include('source.apps.games.urls',
                      namespace="games", app_name="games")),
)

if getattr(settings, "LOCAL_SERVE", False):
    urlpatterns = local_serve_urlpatterns() + urlpatterns
