from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from directory.models import Tag, Creator, Contributor, Series, SeriesAlias, SeriesRating, Volume, Chapter, Translation
from directory.serializers import *

@api_view(['GET', 'POST'])
def series_list(request, format=None):
    '''
    List all series, or create a new series
    '''
    if request.method == 'GET':
        series = Series.objects.all()
        serializer = SeriesSerializer(series, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SeriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def series_detail(request, pk, format=None):
    """
    Retrieve, update or delete a series.
    """
    try:
        series = Series.objects.get(pk=pk)
    except Series.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SeriesSerializer(series)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SeriesSerializer(series, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        series.delete()
        return HttpResponse(status=204)