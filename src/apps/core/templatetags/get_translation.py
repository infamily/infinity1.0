from django import template
from django.template.defaultfilters import stringfilter

from core.models import Translation, Language
from django.contrib.contenttypes.models import ContentType


register = template.Library()

@register.simple_tag()
def get_translation(request_object, language_code, attribute):
    try:
        content_type = ContentType.objects.get_for_model(request_object.__class__)
        language = Language.objects.get(language_code=language_code)
        translation = Translation.objects.get(
            language=language,
            object_id=request_object.id,
            content_type=content_type
        )
        return getattr(translation, attribute)
    except Translation.DoesNotExist:
        return getattr(request_object, attribute)
