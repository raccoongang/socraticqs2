from rest_framework import serializers

from ct.models import Unit


class UnitsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for list of Units.
    """
    unit_id = serializers.SerializerMethodField()
    unit_title = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('unit_id', 'unit_title',)

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
