from rest_framework import generics
from directory.models import Tag, Creator, Contributor, Series, SeriesAlias, SeriesRating, Volume, Chapter, Translation
from directory.serializers import SeriesSerializer

class SeriesList(generics.ListCreateAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

class SeriesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

"""
class SeriesList(APIView):
    '''
    List all series, or create a new series.
    '''
    def get(self, request, format=None):
        series = Series.objects.all()
        serializer = SeriesSerializer(series, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Series(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SeriesDetail(APIView):
    '''
    Retrieve, update or delete a series instance.
    '''
    def get_object(self, pk):
        try:
            return Series.objects.get(pk=pk)
        except Series.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        series = self.get_object(pk)
        serializer = SeriesSerializer(series)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        series = self.get_object(pk)
        serializer = SeriesSerializer(series, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        series = self.get_object(pk)
        series.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

"""
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
    '''
    Retrieve, update or delete a series.
    '''
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
"""