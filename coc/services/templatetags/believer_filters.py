from django import template

register = template.Library()


@register.filter
def answered_count(prayers):
    """Count the number of answered prayers"""
    return sum(1 for prayer in prayers if prayer.answered)
