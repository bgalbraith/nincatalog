from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

from merch import views


urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^search/$", views.search, name="search"),
    re_path(r"^(?P<category_tag>[a-z0-9-]+)/$", views.category, name="category"),
    re_path(
        r"^(?P<category_tag>[a-z0-9-]+)/(?P<product_tag>[a-z0-9-]+)/$",
        views.product,
        name="product",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
