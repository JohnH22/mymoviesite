from django import template
import re

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

@register.filter
def youtube_embed(url):
    """
    Transforms a YouTube URL into an embed.
    """
    if not url:
        return ""
    regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(regex, url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}?enablejsapi=1&origin=http://127.0.0.1:8000"
    return url