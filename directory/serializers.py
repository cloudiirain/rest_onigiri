from rest_framework import serializers
from directory.models import Tag, Creator, Contributor, Series, SeriesAlias, SeriesRating, Volume, Chapter

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series

class SeriesAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesAlias

class SeriesRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesRating

class VolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volume

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter

