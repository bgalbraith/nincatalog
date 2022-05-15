from django import template


register = template.Library()


@register.filter
def track_title(value, artist):
    title = value.name
    if value.artist.lower() != artist.lower():
        title += f' — {value.artist}'

    return title
