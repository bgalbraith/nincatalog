from django.urls import re_path
from django.views.generic import RedirectView

from catalog import views


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^by-(?P<report_tag>[a-z0-9-]+)/$', views.report, name='report'),
    re_path(r'^by-(?P<report_tag>[a-z0-9-]+)/(?P<entry_tag>[a-z0-9-]+)/$',
            views.report_details, name='report_details'),
    re_path(r'^(?P<category_tag>[a-z0-9-]+)/$',
            views.category, name='category'),
    re_path(r'^(?P<category_tag>[a-z0-9-]+)/(?P<item_tag>[a-z0-9-]+)/$',
            views.item, name='item'),
    re_path(r'^default\.asp$', RedirectView.as_view(pattern_name='index')),
    re_path(r'^item\.asp$', views.legacy_item, name='legacy_item'),
]
