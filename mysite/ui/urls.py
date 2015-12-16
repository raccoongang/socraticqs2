from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from ui.views import CourseUnitsVew


urlpatterns = patterns(
    '',
    url(r'hack/$', TemplateView.as_view(template_name='ui/sidebar.html'), name='entry_point'),
    url(r'^api/courses/(?P<course_id>\d+)/units/$', CourseUnitsVew.as_view({'get': 'list'}), name='units_list'),
)
