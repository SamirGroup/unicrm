from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    """
    Split a string by a separator.
    Usage: {{ value|split:', ' }}
    """
    if not value:
        return []
    try:
        return value.split(arg)
    except AttributeError:
        return []

@register.filter(name='first')
def first(value):
    """
    Get the first character of a string.
    Usage: {{ value|first }}
    """
    if value:
        return str(value)[0]
    return ''

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Get an item from a dictionary.
    Usage: {{ dict|get_item:key }}
    """
    if dictionary and key:
        return dictionary.get(key, '')
    return ''

@register.filter(name='sum')
def sum_values(value, arg=None):
    """
    Sum values from a queryset or list.
    Usage: {{ queryset|sum:'field_name' }} or {{ list|sum }}
    """
    if not value:
        return 0
    try:
        # For QuerySet
        if hasattr(value, 'aggregate'):
            from django.db.models import Sum as DBSum
            if arg:
                result = value.aggregate(total=DBSum(arg))
                return result.get('total', 0) or 0
            return 0
        # For list
        elif hasattr(value, '__iter__'):
            total = 0
            for item in value:
                if arg:
                    total += float(getattr(item, arg, 0) or 0)
                else:
                    total += float(item or 0)
            return total
    except (TypeError, ValueError):
        return 0
    return 0
