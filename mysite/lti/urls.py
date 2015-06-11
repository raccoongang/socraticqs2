from django.conf.urls import url, patterns

from lti.views import choice_course_source, create_courseref


urlpatterns = patterns(
    '',
    url(r'(^$|^unit/(?P<unit_id>\d+)/$)', 'lti.views.lti_init', name='lti_init'),
    url(r'^create_courseref/$', create_courseref, name='create_courseref'),
    url(r'^choice_course_source/$', choice_course_source, name='choice_course_source'),
)
