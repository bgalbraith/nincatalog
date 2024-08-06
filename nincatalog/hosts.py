from django_hosts import patterns, host
from django.conf import settings

host_patterns = patterns(
    "",
    host(r"www", "catalog.urls", name="www"),
    host(r"merch", "merch.urls", name="merch"),
    host(r"admin", settings.ROOT_URLCONF, name="admin"),
)
