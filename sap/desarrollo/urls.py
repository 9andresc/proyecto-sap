from django.conf.urls import patterns, url
from desarrollo.views import desarrollo_view

urlpatterns = patterns('',
    url(r'^desarrollo/$', desarrollo_view, name="vista_desarrollo"),
)