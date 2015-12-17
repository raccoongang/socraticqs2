from rest_framework import serializers

from ct.models import CourseUnit, Unit, UnitLesson, Concept, Course


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


class UnitLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitLesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title',)
