from django.conf.urls import include, url
from directory import views

urlpatterns = [
    url(r'^series/$', views.series_list),
    url(r'^series/(?P<pk>[0-9]+)/$', views.series_detail),
]
