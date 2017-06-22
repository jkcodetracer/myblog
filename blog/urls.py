# encoding: utf-8

from django.conf.urls import url
from . import views

# define a namespace, to avoid name conflict
app_name = 'blog'
urlpatterns = [
    url(r'^test$', views.test, name = 'test'),
    url(r'^tagcloud$', views.tagmain, name = 'tags'),
    url(r'^portfome$', views.portfolio, name = 'portfolio'),
    url(r'^aboutme$', views.about, name = 'about'),
    url(r'^$', views.index, name = 'index'),
    #url(r'^$', views.IndexView.as_view(), name = 'index'),
    url(r'^tag/(?P<pk>[0-9]+)$', views.TagView.as_view(), name = 'tag_view'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name = 'detail'),
    url(r'^archieves/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})$', views.archives, name='archives'),
    url(r'^cate/(?P<pk>[0-9]+)$', views.categories, name='archive_cate'),
    url(r'^search/$', views.search, name = 'search'),
]

