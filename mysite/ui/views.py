from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from ct.models import Course, Unit, UnitLesson, Lesson, Role, Concept
from ui.serializers import UnitsSerializer, UnitContentSerializer, CourseSerializer, LessonInfoSerializer, \
    ConceptInfoSerializer, SearchSerializer, CourseSidebarSerializer, InstructorsSerializer, UnitConceptSerializer


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


class CourseSidebarView(mixins.ListModelMixin, viewsets.GenericViewSet):
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
    serializer_class = CourseSidebarSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        queryset = super(CourseSidebarView, self).get_queryset()
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

    def update(self, request, pk):
        ul = get_object_or_404(UnitLesson, id=pk)
        title = request.data.get('title')
        text = request.data.get('raw_text')
        print text
        Lesson.objects.filter(id=ul.lesson.id).update(title=title, text=text)
        serializer = LessonInfoSerializer(ul)
        return Response(serializer.data)

    def create(self, request):
        title = request.data.get('title')
        text = request.data.get('raw_text')
        user_id = request.data.get('author')
        unit_id = request.data.get('unit_id')
        print user_id
        lesson = Lesson.objects.create(title=title,
                                       text=text,
                                       treeID=1,
                                       addedBy=User.objects.get(id=user_id))
        unit = Unit.objects.get(id=unit_id)
        ul = UnitLesson.create_from_lesson(lesson, unit)
        serializer = LessonInfoSerializer(ul)
        return Response(serializer.data)


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


class CourseView(viewsets.ModelViewSet):
    """
    API for getting course data

    Response:
    {
    "title",
    "description",
    "added_by"
    }
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    filters = ['addedBy']

    def get_queryset(self):
        queryset = super(CourseView, self).get_queryset()
        query_filter = {}
        for each in self.filters:
            if each in self.request.GET:
                query_filter[each] = self.request.GET[each]
        queryset = queryset.filter(**query_filter)
        return queryset


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


class UnitConceptView(viewsets.ModelViewSet):
    """
    API for Concept
    Response:
    {
    }
    """
    queryset = UnitLesson.objects.all()
    serializer_class = ConceptInfoSerializer

    def get_queryset(self):
        queryset = super(UnitConceptView, self).get_queryset()

        if 'unit_id' in self.kwargs:
            unit_id = self.kwargs['unit_id']
            queryset = queryset.filter(unit_id=unit_id) \
                               .exclude(lesson__isnull=True) \
                               .exclude(lesson__concept__isnull=True)
        return queryset

    def update(self, request, pk):
        ul = get_object_or_404(UnitLesson, id=pk)
        title = request.data.get('title')
        text = request.data.get('text')
        Lesson.objects.filter(id=ul.lesson.id).update(title=title, text=text)
        serializer = ConceptInfoSerializer(ul)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        unit = Unit.objects.get(id=self.kwargs['unit_id'])
        concept = Concept.new_concept(request.data.get('title'),
                            request.data.get('text'),
                            unit,
                            User.objects.get(id=request.data.get('added_by')))

        lesson = Lesson.objects.create(title=request.data.get('title'),
                                       text=request.data.get('text'),
                                       addedBy=User.objects.get(id=request.data.get('added_by')))
        lesson.save_root(concept)
        ul = UnitLesson.create_from_lesson(lesson, unit)

        serializer = LessonInfoSerializer(ul)
        return Response(serializer.data)
