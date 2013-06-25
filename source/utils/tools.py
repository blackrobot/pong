from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


def local_serve_urlpatterns():
    re = r"^%s(?P<path>.*)$" % settings.MEDIA_URL.lstrip('/')
    options = {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}

    return patterns('django.views.static',
                    url(re, 'serve', options)) + staticfiles_urlpatterns()
