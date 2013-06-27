from django.conf.urls.defaults import patterns, url


RESET_REGEX = r'-'.join([
    r'(?P<uidb36>[0-9A-Za-z]{1,13})',
    r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
])


urlpatterns = patterns(
    'django.contrib.auth.views',

    # Login/Logout
    url(r"^login/$", 'login', name="login"),
    url(r"^logout/$", 'logout', name="logout"),

    # Change password
    url(r"^change-password/$", 'password_change',
        {'post_change_redirect': '/accounts/change-password/done/'},
        name="password_change"),
    url(r"^change-password/done/$", 'password_change_done',
        name="password_change_done"),

    # Reset password
    url(r"^reset-password/$", 'password_reset',
        {'post_reset_redirect': '/accounts/reset-password/done/'},
        name="password_reset"),
    url(r"^reset-password/done/$", 'password_reset_done',
        name="password_reset_done"),
    url(r"^reset-password/confirm/{}/$".format(RESET_REGEX),
        'password_reset_confirm',
        {'post_reset_redirect': '/accounts/reset-password/complete/'},
        name="password_reset_confirm"),
    url(r"^reset-password/complete/$", 'password_reset_complete',
        name="password_reset_complete"),
)
