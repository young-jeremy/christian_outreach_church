from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    """Subtract the arg from the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return value


@register.filter
def divisibleby(value, arg):
    """Return the percentage of value/arg * 100."""
    try:
        return int(value) / int(arg) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
