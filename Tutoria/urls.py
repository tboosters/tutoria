from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from django.views.decorators.csrf import csrf_exempt

import Administrator
import Search
import UserAccount
import Bookings

# Urls for the base Tutoria applications
urlpatterns = [
    # Admin site url redirect
    url(r'^admin/', admin.site.urls),

    # Url redirects for Search App
    url(r'^search/', include('Search.urls')),
    # Url redirects for UserAccount App
    url(r'^account/', include('UserAccount.urls')),
    # Url redirects for Bookings App
    url(r'^booking/', include('Bookings.urls')),
    # Url redirects for Administrator App
    url(r'^administrator/', include('Administrator.urls')),
    # Url redirects for Wallet App
    url(r'^wallet/', include('Wallet.urls')),

    # Homepage url redirect
    url(r'^$', Search.views.index, name='index'),

    # User authentication url redirects
    url(r'^login', csrf_exempt(UserAccount.views.login), name='login'),
    url(r'^logout', csrf_exempt(UserAccount.views.logout), name='logout'),
    url(r'^signup', csrf_exempt(UserAccount.views.signup), name='signup'),
    url(r'^editProfile', csrf_exempt(UserAccount.views.editProfile), name='editProfile'),

    # Password reset redirects
    url(r'^requestResetToken', csrf_exempt(Administrator.views.requestResetToken), name='requestResetToken'),
    url(r'^verifyToken', csrf_exempt(Administrator.views.verifyToken), name='verifyToken'),
    url(r'^resetPassword', csrf_exempt(Administrator.views.resetPassword), name='resetPassword'),

    #forgot password template
    url(r'^forgotPassword', TemplateView.as_view(template_name='forgotPassword.html'))
]
