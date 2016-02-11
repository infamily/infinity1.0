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
		return [{'': {'f_price': u'',
                      'f_units': u'',
                      'max_price': u'',
                      'max_units': u'',
                      'min_price': u'',
                      'min_units': u'',
                      'price_unit': u''}}]
