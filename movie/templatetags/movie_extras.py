from django import template

register = template.Library()

@register.filter
def format_duration(minutes):
    if not minutes:
        return ""
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if hours > 0:
        return f"{hours}h {remaining_minutes:02d}min"
    return f"{remaining_minutes}min"