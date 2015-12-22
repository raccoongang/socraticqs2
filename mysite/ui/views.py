from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ct.models import Course, Unit, UnitLesson, ConceptLink, Lesson, Concept
from ui.serializers import UnitsSerializer, UnitContentSerializer, CourseSerializer, LessonInfoSerializer, \
    ConceptInfoSerializer


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


class CourseView(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API returning courses item(lesson, concept)

    Response:
    [
    {
    'ul_id',
    'title',
    }
    ]

    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        queryset = super(CourseView, self).get_queryset()
        if self.request.user:
            queryset = Course.objects.filter(addedBy=self.request.user)
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


class LessonContentView(viewsets.ModelViewSet):
    """
    API for getting lesson content
    Filter paramenter:
    `unit_id`

    Response:

    [
    {
        "id": 1,
        "title",
        "text",
        "added_by"
        "order"
    },
    ]
    """
    serializer_class = LessonInfoSerializer
    queryset = Lesson.objects.all()

    def get_queryset(self):
        queryset = UnitLesson.objects.all()
        if 'unit_id' in self.request.GET:
            queryset = UnitLesson.objects.filter(unit_id=self.request.GET['unit_id'])
        return queryset


class ConceptContentView(viewsets.ModelViewSet):
    """
    API for getting concept content
    Filter paramenter:
    `unit_id`

    Response:

    [
    {
        "id": 1,
        "title",
        "text",
        "added_by"
        "order"
    },
    ]
    """
    serializer_class = ConceptInfoSerializer
    queryset = Concept.objects.all()

    def get_queryset(self):
        queryset = ConceptLink.objects.all()
        if 'unit_id' in self.request.GET:
            queryset = ConceptLink.objects.filter(unit_id__in=[x['id'] for x in UnitLesson.objects.filter(
                unit_id=self.request.GET['unit_id']).values(('id',))])

        return queryset

    def get_object(self):
        return ConceptLink.objects.filter(lesson=UnitLesson.objects.filter(
            id=self.kwargs[self.lookup_field]).first()).first()
