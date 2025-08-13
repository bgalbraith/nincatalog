from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def upc_url(value):
    value = value.replace(' ', '')
    value = value.replace('-', '')
    if len(value) == 12:
        value = f"0{value}"
    return f"https://www.barcodelookup.com/{value}"