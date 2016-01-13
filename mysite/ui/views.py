from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from ct.models import Course, Unit, UnitLesson, Lesson, Role
from ui.serializers import UnitsSerializer, UnitContentSerializer, CourseSerializer, LessonInfoSerializer, \
    ConceptInfoSerializer, SearchSerializer, CourseInfoSerializer, InstructorsSerializer


class CourseUnitsView(mixins.ListModelMixin, viewsets.GenericViewSet):
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
        queryset = super(CourseUnitsView, self).get_queryset()
        course_id = self.kwargs.get('course_id')
        if course_id:
            course = Course.objects.filter(id=course_id).first()
            if course:
                queryset = course.get_course_units(publishedOnly=False)
        return queryset


class CourseView(mixins.ListModelMixin, viewsets.GenericViewSet):
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


class UnitContentView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
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
    serializer_class = UnitContentSerializer
    queryset = Unit.objects.all()

    def retrieve(self, request, unit_id=None):
        queryset = Unit.objects.all()
        unit = get_object_or_404(queryset, pk=unit_id)
        serializer = UnitContentSerializer(unit)
        return Response(serializer.data)

    def append(self, request, unit_id=None):
        ul_id = request.data.get('ul_id')
        order = request.data.get('order')

        if not isinstance(ul_id, int) and ul_id is not None:
            ul_id = int(ul_id)

        if not isinstance(order, int) and order is not None:
            order = int(order)

        ul = get_object_or_404(UnitLesson, pk=ul_id)
        unit = get_object_or_404(Unit, pk=unit_id)
        ul = unit.append(ul, request.user)
        if order is not None:
            unit.reorder_exercise(old=ul.order, new=order)
        serializer = UnitContentSerializer(unit)
        return Response(serializer.data)


class LessonInfoView(viewsets.ModelViewSet):
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
            queryset = queryset.filter(unit_id=self.request.GET['unit_id'])
        return queryset


class ConceptInfoView(viewsets.ModelViewSet):
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
    queryset = UnitLesson.objects.filter(lesson__concept__isnull=False)

    def get_queryset(self):
        queryset = super(ConceptInfoView, self).get_queryset()
        if 'unit_id' in self.request.GET:
            queryset = queryset.filter(unit_id=self.request.GET['unit_id'])
        return queryset

    def get_object(self):
        return UnitLesson.objects.filter(pk=self.kwargs[self.lookup_field]).first()


class SearchView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """API for serching through unit lessons

    Response format:

    [
      {
       'ul_id'
       'title'
       'type'
       'ul_addedby'
      }
    ]
    """
    queryset = UnitLesson.objects.all()
    serializer_class = SearchSerializer

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        if 'text' in self.request.GET:
            queryset = UnitLesson.search_text(self.request.GET['text'])
        else:
            queryset = []
        return queryset


class CourseInfoView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    API for getting course data

    Response:
    {
    "title",
    "description",
    "added_by"
    }
    """
    serializer_class = CourseInfoSerializer
    queryset = Course.objects.all()


class InstructorView(viewsets.ModelViewSet):
    """
    Returns Instructors list.
    """
    queryset = User.objects.all()
    serializer_class = InstructorsSerializer

    def get_queryset(self):
        queryset = super(InstructorView, self).get_queryset()
        queryset = queryset.filter(id__in=set([role.user.id for role in Role.objects.filter(role=Role.INSTRUCTOR)]))
        return queryset
