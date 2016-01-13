from django.conf.urls import patterns, include, url
from django.apps import apps
from rest_framework.routers import SimpleRouter

from mysite.views import *
from issues.views import (
    IssuesView,
    IssueLabelsView,
    IssueCommentsView
)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

router = SimpleRouter()
router.register(r'api/issues', IssuesView)
router.register(r'api/labels', IssueLabelsView)
router.register(r'api/comments', IssueCommentsView)

urlpatterns = patterns(
    '',
    (r'^$', home_page),
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    (r'^ct/', include('ct.urls', namespace='ct')),
    (r'^fsm/', include('fsm.urls', namespace='fsm')),
    (r'^ui/', include('ui.urls', namespace='ui')),

    # Login / logout.
    (r'^login/$', 'psa.views.custom_login'),
    (r'^logout/$', logout_page, {'next_page': '/login/'}),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    url(r'^email-sent/$', 'psa.views.validation_sent'),
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^tmp-email-ask/$', 'psa.views.ask_stranger'),
    url(r'^set-pass/$', 'psa.views.set_pass'),

    url(r'^done/$', 'psa.views.done'),

    # REST API
    url(r'^', include(router.urls)),
)

if apps.is_installed('lti'):
    urlpatterns += patterns(
        '',
        url(r'^lti/', include('lti.urls', namespace='lti')),
    )
