from django.conf.urls import patterns, url

from ui.views import CourseUnitsVew


urlpatterns = patterns(
    '',
    url(r'^api/courses/(?P<course_id>\d+)/units/$', CourseUnitsVew.as_view({'get': 'list'}), name='units_list'),
)
