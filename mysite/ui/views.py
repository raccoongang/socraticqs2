from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ct.models import Course, Unit
from ui.serializers import UnitsSerializer, UnitContentSerializer


class CourseUnitsVew(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    """API for getting course units

    Response format:

    [
      {
       'unit_id'
       'unit_title'
       'order'
      },
      {
       'unit_id'
       'unit_title'
       'order'
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


class UnitContentVew(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """API for getting Unit content: Lessons, Concepts

    Response format:
    {
      'id'
      'lessons': [
         {'id', 'lesson_title, 'order'}
      ]
      'concepts': [
        {'id', 'title'}
      ]
    }
    """
    def retrieve(self, request, unit_id=None):
        queryset = Unit.objects.all()
        unit = get_object_or_404(queryset, pk=unit_id)
        serializer = UnitContentSerializer(unit)
        return Response(serializer.data)
