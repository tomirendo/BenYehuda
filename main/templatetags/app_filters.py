from django.template import Library
from django.utils.safestring import mark_safe

register = Library()
@register.filter(name = "json_filter")
def json_filter(obj):
    from json import dumps
    return mark_safe(dumps([i.object.to_dict() for i in obj]))

#filters.FILTERS['json_filter'] = json_filter
#register.filter('json_filter', json_filter)
