from django.conf import settings
from django.urls import re_path, include
from django.conf.urls.static import static
from django.contrib import admin

from catalog.views import handle404


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include('catalog.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = handle404
