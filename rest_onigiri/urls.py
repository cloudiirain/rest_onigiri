from django.conf.urls import include, url
from django.contrib import admin

from moderation.helpers import auto_discover
auto_discover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'rest_onigiri.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('directory.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
