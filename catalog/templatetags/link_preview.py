"""Helpers for the Open Graph tags that drive link previews (issue #57)."""

import html
import re

from django import template
from django.utils.html import strip_tags
from django.utils.text import Truncator

from catalog.templatetags.markdown import markdown

register = template.Library()


@register.simple_tag(takes_context=True)
def absolute_uri(context, url):
    """Previews are fetched by other services, so image URLs must be absolute."""
    return context["request"].build_absolute_uri(url)


@register.filter
def preview_text(value, length=200):
    """Markdown to one line of plain text, cut to `length` characters.

    Entities are unescaped so autoescaping encodes them exactly once.
    """
    text = html.unescape(strip_tags(markdown(value or "")))
    return Truncator(re.sub(r"\s+", " ", text).strip()).chars(length)
