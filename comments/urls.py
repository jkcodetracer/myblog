# encoding: utf-8

from django.conf.urls import url

from . import views

app_name = 'comments'
urlpatterns = [
    url(r'^comment/post/(?P<pk>[0-9]+)/$', views.article_comment, name = "article_comments"),
]


