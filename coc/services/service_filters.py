from django import template

register = template.Library()


@register.filter
def format_duration(duration):
    """
    Format a timedelta object into a human-readable string.
    Example: 1:30:00 becomes "1 hour 30 minutes"
    """
    if not duration:
        return "0 minutes"

    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    parts = []
    if hours == 1:
        parts.append("1 hour")
    elif hours > 1:
        parts.append(f"{hours} hours")

    if minutes == 1:
        parts.append("1 minute")
    elif minutes > 0:
        parts.append(f"{minutes} minutes")

    if not parts:  # Less than a minute
        return "Less than a minute"

    return " ".join(parts)
