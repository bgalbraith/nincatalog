from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from catalog import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^by-(?P<report_tag>[a-z0-9-]+)/$', views.report, name='report'),
    url(r'^by-(?P<report_tag>[a-z0-9-]+)/(?P<entry_tag>[a-z0-9-]+)/$',
        views.report_details, name='report_details'),
    url(r'^(?P<category_tag>[a-z0-9-]+)/$', views.category, name='category'),
    url(r'^(?P<category_tag>[a-z0-9-]+)/(?P<item_tag>[a-z0-9-]+)/$',
        views.item, name='item'),
    url(r'^default\.asp$', RedirectView.as_view(pattern_name='index')),
    url(r'^item\.asp$', views.legacy_item, name='legacy_item'),
)
