from django.conf.urls import patterns, include, url
from django.apps import apps
from mysite.views import *

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
    (r'^chat/', include('chat.urls', namespace='chat')),

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
)

if apps.is_installed('lti'):
    urlpatterns += patterns(
        '',
        url(r'^lti/', include('lti.urls', namespace='lti')),
    )


def handler404(request):
    response = render(
        request,
        'lti/error.html',
        {'message': 'Requested resource is not found.'}
    )
    response.status_code = 404
    return response


def handler500(request):
    response = render(
        request,
        'lti/error.html',
        {'message': 'Something goes wrong but we are working hard to fix this.'}
    )
    response.status_code = 500
    return response
