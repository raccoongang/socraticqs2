from django.conf.urls import patterns, include, url
from django.apps import apps
from mysite.views import *

from psa.views import RegisterView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', home_page),
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    (r'^ct/', include('ct.urls', namespace='ct')),
    (r'^fsm/', include('fsm.urls', namespace='fsm')),

    # Login / logout.
    (r'^login/$', 'psa.views.custom_login'),
    (r'^logout/$', logout_page, {'next_page': '/login/'}),
    (r'^register/$', RegisterView.as_view()),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    url(r'^email-sent/$', 'psa.views.validation_sent'),
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^tmp-email-ask/$', 'psa.views.ask_stranger'),
    url(r'^set-pass/$', 'psa.views.set_pass'),
    url(r'^forgot-pass/$', 'psa.views.forgot_pass'),
    url(r'^reset-pass/(?P<reset_token>[^/]+)/$', 'psa.views.reset_pass', name='reset-password'),



    url(r'^done/$', 'psa.views.done'),
)

if apps.is_installed('lti'):
    urlpatterns += patterns(
        '',
        url(r'^lti/', include('lti.urls', namespace='lti')),
    )
