from django import template
import os
from django.conf import settings


register = template.Library()


@register.simple_tag
def static_postfix(file):
    pf = os.path.splitext(file)[1].replace('.', '')
    if pf == 'js':
        return os.path.getsize(os.path.join(settings.STATIC_ROOT, 'js/' + file))
    if pf == 'css':
        return os.path.getsize(os.path.join(settings.STATIC_ROOT, 'css/' + file))
    return 0

