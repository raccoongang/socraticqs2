from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter

from ui.views import (
    CourseUnitsView,
    UnitContentView,
    CourseView,
    LessonInfoView,
    ConceptInfoView,
    SearchView,
    CourseInfoView,
)

router = SimpleRouter()
router.register(r'api/lesson', LessonInfoView)
router.register(r'api/concept', ConceptInfoView)
router.register(r'api/search', SearchView, base_name='search')
router.register(r'api/course', CourseInfoView)


urlpatterns = patterns(
    '',
    url(r'^hack/$', TemplateView.as_view(template_name='ui/sidebar.html'), name='entry_point'),
    url(r'^api/courses/(?P<course_id>\d+)/units/$', CourseUnitsView.as_view({'get': 'list'}), name='units_list'),
    url(
        r'^api/units/(?P<unit_id>\d+)/content/$',
        UnitContentView.as_view({'get': 'retrieve', 'put': 'append'}),
        name='unit_content'
    ),
    url(r'^api/courses/', CourseView.as_view({'get': 'list'}), name='course_list'),
    url(r'^', include(router.urls)),
)
