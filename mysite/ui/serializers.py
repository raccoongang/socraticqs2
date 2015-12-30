from rest_framework import serializers
from django.utils.safestring import mark_safe

from ct.models import CourseUnit, Unit, UnitLesson, Concept, Course, Lesson
from ct.templatetags.ct_extras import md2html
from ui.models import Issue, IssueLabel


class UnitsSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for list of Units

    In current implementation this is a CourseUnit models
    that hides Unit.
    """
    unit_id = serializers.SerializerMethodField()
    unit_title = serializers.SerializerMethodField()

    class Meta:
        model = CourseUnit
        fields = ('unit_id', 'unit_title', 'order')

    def get_unit_id(self, obj):
        """
        Return CourseUnit -> unit.id
        """
        return obj.unit.id

    def get_unit_title(self, obj):
        """
        Return CourseUnit -> unit.title
        """
        return obj.unit.title


class LessonsSerializer(serializers.ModelSerializer):
    """
    Units aka UnitLessons serializer.
    """
    lesson_title = serializers.SerializerMethodField()

    class Meta:
        model = UnitLesson
        fields = ('id', 'lesson_title', 'order')

    def get_lesson_title(self, obj):
        """
        Returning Lesson id
        """
        return obj.lesson.title


class ConceptsSerializer(serializers.ModelSerializer):
    """
    Units aka UnitLessons serializer.
    """
    ul_id = serializers.SerializerMethodField()

    class Meta:
        model = Concept
        fields = ('ul_id', 'title')

    def get_ul_id(self, obj):
        """
        Returning UnitLesson id for this Concept.
        """
        return UnitLesson.objects.filter(lesson__concept=obj).first().id


class UnitContentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Unit content: Lessons, Concepts.
    """
    lessons = serializers.SerializerMethodField()
    concepts = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'lessons', 'concepts')

    def get_lessons(self, obj):
        """
        Returning list of Lessons for this Unit.
        """
        return LessonsSerializer(many=True).to_representation(obj.get_exercises())

    def get_concepts(self, obj):
        """
        Returning list of related Concepts for this Unit.
        """
        return ConceptsSerializer(many=True).to_representation(obj.get_related_concepts().keys())


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title',)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'text', 'addedBy')


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept


class SearchSerializer(serializers.ModelSerializer):
    """
    Serializer for search results
    """
    title = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    kind = serializers.SerializerMethodField()

    class Meta:
        model = UnitLesson
        fields = ('id', 'title', 'kind', 'author')

    def get_title(self, obj):
        return obj.lesson.title

    def get_author(self, obj):
        return obj.addedBy.username

    def get_kind(self, obj):
        return dict(Lesson.KIND_CHOICES)[obj.lesson.kind]


class LessonInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for lesson data
    """
    title = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    added_by = serializers.SerializerMethodField()

    class Meta:
        model = UnitLesson
        fields = ('id', 'title', 'text', 'added_by', 'order')

    def get_title(self, obj):
        return Lesson.objects.filter(id=obj.lesson.id).first().title

    def get_text(self, obj):
        return mark_safe(md2html(Lesson.objects.filter(id=obj.lesson.id).first().text))

    def get_added_by(self, obj):
        return obj.addedBy.username


class ConceptInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for concept data
    """
    title = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    added_by = serializers.SerializerMethodField()

    class Meta:
        model = UnitLesson
        fields = ('id', 'title', 'text', 'added_by')

    def get_title(self, obj):
        return obj.lesson.concept.title

    def get_text(self, obj):
        return mark_safe(md2html(obj.lesson.text))

    def get_added_by(self, obj):
        return obj.addedBy.username


class CourseInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for retrive course data
    """
    added_by = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('title', 'description', 'added_by')

    def get_added_by(self, obj):
        return obj.addedBy.username


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer for Issue model.
    """
    related = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    assignee_name = serializers.SerializerMethodField()

    class Meta:
        model = Issue

    def get_related(self, obj):
        if type(obj.related) == Course:
            return CourseSerializer(obj.related).data
        elif type(obj.related) == CourseUnit:
            return UnitsSerializer(obj.related).data
        elif type(obj.related) == UnitLesson:
            return LessonInfoSerializer(obj.related).data

    def get_author_name(self, obj):
        return obj.author.username

    def get_assignee_name(self, obj):
        return obj.author.username


class IssueLabelSerializer(serializers.ModelSerializer):
    """
    Serializer for IssueLabels restAPI
    """
    class Meta:
        model = IssueLabel