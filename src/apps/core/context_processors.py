from django.conf import settings
from django.utils.translation import pgettext

def language_domains(request):
    values = {
        'base_domain': settings.BASE_DOMAIN,
        'languages_domains': settings.LANGUAGES_DOMAINS,
    }
    return values
