from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter

from ui.views import CourseUnitsVew, UnitContentVew, CourseView, LessonInfoView, ConceptInfoView, SearchView

router = SimpleRouter()
router.register(r'api/lesson', LessonInfoView)
router.register(r'api/concept', ConceptInfoView)
router.register(r'api/search', SearchView, base_name='search')


urlpatterns = patterns(
    '',
    url(r'^hack/$', TemplateView.as_view(template_name='ui/sidebar.html'), name='entry_point'),
    url(r'^api/courses/(?P<course_id>\d+)/units/$', CourseUnitsVew.as_view({'get': 'list'}), name='units_list'),
    url(r'^api/units/(?P<unit_id>\d+)/content/$', UnitContentVew.as_view({'get': 'retrieve'}), name='unit_content'),
    url(r'^api/courses/', CourseView.as_view({'get': 'list'}), name='course_list'),
    url(r'^', include(router.urls)),
)
