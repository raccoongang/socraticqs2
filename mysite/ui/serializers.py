from rest_framework import serializers
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from ct.models import CourseUnit, Unit, UnitLesson, Concept, Course, Lesson
from ct.templatetags.ct_extras import md2html


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


class CourseSidebarSerializer(serializers.ModelSerializer):
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
    raw_text = serializers.SerializerMethodField()
    added_by = serializers.SerializerMethodField()

    class Meta:
        model = UnitLesson
        fields = ('id', 'title', 'text', 'raw_text', 'added_by', 'order')

    def get_title(self, obj):
        return Lesson.objects.filter(id=obj.lesson.id).first().title

    def get_text(self, obj):
        return mark_safe(md2html(Lesson.objects.filter(id=obj.lesson.id).first().text))

    def get_raw_text(self, obj):
        return Lesson.objects.filter(id=obj.lesson.id).first().text

    def get_added_by(self, obj):
        return obj.addedBy.username


class ConceptInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for concept data
    """
    title = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    added_by = serializers.SerializerMethodField()
    concept_id = serializers.SerializerMethodField()

    class Meta:
        model = UnitLesson
        fields = ('id', 'concept_id', 'title', 'text', 'added_by')

    def get_concept_id(self, obj):
        return obj.lesson.concept.id

    def get_title(self, obj):
        return obj.lesson.title

    def get_text(self, obj):
        return mark_safe(md2html(obj.lesson.text))

    def get_added_by(self, obj):
        return obj.addedBy.username


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for retrive course data
    """
    added_by = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'added_by', 'addedBy')

    def get_added_by(self, obj):
        return obj.addedBy.username


class InstructorsSerializer(serializers.ModelSerializer):
    """
    Instructor serizlizer.
    """
    class Meta:
        model = User
        fields = ('id', 'username')


class ConceptTitleSerializer(serializers.ModelSerializer):
    """
    Concept Serialize
    """
    title = serializers.SerializerMethodField()
    concept_id = serializers.SerializerMethodField()

    class Meta:
        model = UnitLesson
        fields = ('concept_id', 'title')

    def get_title(self, obj):
        return obj.lesson.title

    def get_concept_id(self, obj):
        return obj.lesson.concept.id


class LessonTitleSerializer(serializers.ModelSerializer):
    """
    Lesson list Serialize
    """
    title = serializers.SerializerMethodField()

    class Meta:
        model = UnitLesson
        fields = ('id', 'title')

    def get_title(self, obj):
        return obj.lesson.title
