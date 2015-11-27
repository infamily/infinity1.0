from django import template
from django.template.defaultfilters import stringfilter

from core.models import Vote

register = template.Library()

@register.filter
def cut(comment, user_id):
    """Removes all values of arg from the given string"""
    if comment.user_vote(user_id):
        return comment.user_vote(user_id).value
    else:
        return 0
