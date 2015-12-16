from rest_framework import viewsets

from ct.models import Course
from ui.serializers import UnitsSerializer


class CourseUnitsVew(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API for getting course units.

    Response format:

    [
      {
       'unit_id'
       'unit_title'
      },
      {
       'unit_id'
       'unit_title'
      },
    ]
    """
    queryset = Course.objects.all()
    serializer_class = UnitsSerializer

    def get_queryset(self):
        queryset = super(CourseUnitsVew, self).get_queryset()
        course_id = self.kwargs.get('course_id')
        if course_id:
            course = Course.objects.filter(id=course_id).first()
            if course:
                queryset = course.get_course_units(publishedOnly=False)
        return queryset
