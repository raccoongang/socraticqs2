from rest_framework import serializers

from ct.models import CourseUnit, Course, UnitLesson
from issues.models import Issue, IssueLabel, IssueComment
from ui.serializers import CourseSerializer, UnitsSerializer, LessonInfoSerializer


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
        return obj.assignee.username if obj.assignee is not None else None


class IssueLabelSerializer(serializers.ModelSerializer):
    """
    Serializer for IssueLabels restAPI
    """
    class Meta:
        model = IssueLabel


class IssueCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for IssueLabels restAPI
    """
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = IssueComment

    def get_author_name(self, obj):
        return obj.author.username
