from django.conf import settings
from django.urls import re_path
from django.conf.urls.static import static
from django.contrib import admin

from catalog.views import handle404


urlpatterns = [re_path(r"^", admin.site.urls)] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

handler404 = handle404
