from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def upc_url(value):
    value = value.replace(' ', '')
    value = value.replace('-', '')
    return "http://www.upcdatabase.com/item.asp?upc=" + value