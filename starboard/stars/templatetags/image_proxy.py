from camo_sign import create_signed_url
from django import template
from django.conf import settings

register = template.Library()


@register.filter
def proxy(url):
    """Pass an image url through camo"""
    return create_signed_url(settings.CAMO_URL, hmac_key=settings.CAMO_KEY, url=url)
