from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import SimpleRouter

from ui.views import (
    UnitView,
    UnitContentView,
    CourseView,
    LessonInfoView,
    ConceptInfoView,
    SearchView,
    CourseSidebarView,
    InstructorView,
    ConceptView,
    RelatedLessonView,
    RelatedConceptView
)

router = SimpleRouter()
router.register(r'api/lesson', LessonInfoView, base_name='lessons')
router.register(r'api/concept', ConceptInfoView, base_name='concept')
router.register(r'api/search', SearchView, base_name='search')
router.register(r'api/courses', CourseView, base_name='courses')
router.register(r'api/concepts', ConceptView, base_name='concepts')
router.register(r'api/units', UnitView, base_name='units')
router.register(r'api/related-lesson', RelatedLessonView, base_name='related-lesson')
router.register(r'api/related-concept', RelatedConceptView, base_name='related-concept')



urlpatterns = patterns(
    '',
    url(
        r'^hack/.*$',
        login_required(TemplateView.as_view(template_name='ui/hack.html')),
        name='entry_point'
    ),
    url(
        r'^api/units/(?P<unit_id>\d+)/content/$',
        UnitContentView.as_view({'get': 'retrieve', 'put': 'append'}),
        name='unit_content'
    ),
    url(r'^api/courses_for_sidebar/', CourseSidebarView.as_view({'get': 'list'}), name='course_list'),
    url(r'^api/assignee/', InstructorView.as_view({'get': 'list'}), name='assignee_list'),
    url(r'^', include(router.urls)),
)
