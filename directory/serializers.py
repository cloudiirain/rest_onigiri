from rest_framework import serializers
from django.contrib.auth.models import User
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

class SeriesSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    sort_key = serializers.CharField(required=False, allow_blank=True, max_length=100)
    #contributors
    #tags
    hitcount = serializers.IntegerField(read_only=True)
    synopsis = serializers.CharField(required=False, allow_blank=True)
    image = serializers.URLField(required=False, allow_blank=True)

    def create(self, validated_data):
        '''
        Create and return a new `Series` instance, given the validated data.
        For now, automoderate everything
        '''
        series = Series.objects.create(**validated_data)
        admin = User.objects.get(username='admin')
        series.moderated_object.approve(moderated_by=admin, reason='test')
        return series

    def update(self, instance, validated_data):
        '''
        Update and return an existing `Series` instance, given the validated data.
        For now, automoderate everything
        '''
        instance.name = validated_data.get('name', instance.name)
        instance.sort_key = validated_data.get('sort_key', instance.sort_key)
        instance.synopsis = validated_data.get('synopsis', instance.synopsis)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        admin = User.objects.get(username='admin')
        instance.moderated_object.approve(moderated_by=admin, reason='test')
        return instance

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

