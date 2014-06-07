from django.conf.urls import patterns, url

from catalog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<category_tag>[a-z0-9-]+)/$', views.category, name='category'),
    url(r'^(?P<category_tag>[a-z0-9-]+)/(?P<item_tag>[a-z0-9-]+)/$', views.item,
        name='item'),
)
