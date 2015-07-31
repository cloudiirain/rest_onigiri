from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from directory.models import Tag, Creator, Contributor, Series, SeriesAlias, SeriesRating, Volume, Chapter, Translation
from directory.serializers import *

class JSONResponse(HttpResponse):
    '''
    An HttpResponse that renders its content into JSON.
    '''
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def series_list(request):
    '''
    List all series, or create a new series
    '''
    if request.method == 'GET':
        series = Series.objects.all()
        serializer = SeriesSerializer(series, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SeriesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def series_detail(request, pk):
    """
    Retrieve, update or delete a series.
    """
    try:
        series = Series.objects.get(pk=pk)
    except Series.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SeriesSerializer(series)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SeriesSerializer(series, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        series.delete()
        return HttpResponse(status=204)