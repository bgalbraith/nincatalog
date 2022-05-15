from datetime import timedelta

from django import template


register = template.Library()


@register.filter
def track_length(value):
    if value == timedelta(seconds=0):
        return ''
    
    duration = value.total_seconds() // 1000    
    return f'{int(duration // 60):02d}:{int(duration % 60):02d}'
