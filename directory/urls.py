from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from directory import views

urlpatterns = [
    url(r'^series/$', views.SeriesList.as_view()),
    url(r'^series/(?P<pk>[0-9]+)/$', views.SeriesDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
