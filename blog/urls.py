# encoding: utf-8

from django.conf.urls import url
from . import views

# define a namespace, to avoid name conflict
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name = 'detail'),
    url(r'^archieves/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})$', views.archives, name='archives'),
]

