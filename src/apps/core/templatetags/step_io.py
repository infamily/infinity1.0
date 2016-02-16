from django import template
from django.template.defaultfilters import stringfilter

import stepio

register = template.Library()

@register.filter
def step_io(request_object):
    try:
        return stepio.parse(request_object)
    except:
        # return stepio.parse(':~')
		return False
