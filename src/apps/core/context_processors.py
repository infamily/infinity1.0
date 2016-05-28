from django.conf import settings

def language_domains(request):
    values = {
        'main_domain': settings.MAIN_DOMAIN,
        'languages_domains': settings.LANGUAGES_DOMAINS,
    }
    return values
