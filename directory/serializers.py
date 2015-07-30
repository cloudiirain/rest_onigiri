from rest_framework import serializers
from directory.models import Series, Volume, Chapter

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ('id', 'name', 'synopsis')