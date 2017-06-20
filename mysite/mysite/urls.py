from django.conf.urls import patterns, include, url
from django.conf import settings
from django.apps import apps

from mysite.views import *
from pages.views import interested_form

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


from social.utils import setting_name
from psa.views import complete


extra = getattr(settings, setting_name('TRAILING_SLASH'), True) and '/' or ''

urlpatterns = patterns(
    '',
    url(r'^ct/', include('ct.urls', namespace='ct')),
    url(r'^fsm/', include('fsm.urls', namespace='fsm')),
    url(r'^chat/', include('chat.urls', namespace='chat')),
    url(r'^lms/', include('lms.urls', namespace='lms')),

    # Login / logout.
    url(r'^login/$', 'psa.views.custom_login', name='login'),
    url(r'^logout/$', logout_page, {'next_page': '/login/'}, name='logout'),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    url(r'^email-sent/$', 'psa.views.validation_sent'),
    url(r'^complete/email{0}$'.format(extra), complete,
        name='complete'),
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^tmp-email-ask/$', 'psa.views.ask_stranger'),
    url(r'^set-pass/$', 'psa.views.set_pass'),

    url(r'^done/$', 'psa.views.done'),
    url(r'^lti/', include('lti.urls', namespace='lti')),
    url(r'^interested-form/', interested_form, name='interested-form'),
    # Base API
    url(r'^api/', include('api.urls', namespace='api')),
    # CMS
    url(r'^', include('cms.urls')),
)


if settings.DEBUG:
    urlpatterns += [
        url(r'markup/(?P<path>.*)$', markup_view),
        url(
            r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ]
    try:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        print "No django-debug-toolbar installed. Running without it..."
