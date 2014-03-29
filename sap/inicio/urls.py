from django.conf.urls import patterns, url
from inicio.views import archive

urlpatterns = patterns('', url(r'^$', archive),)