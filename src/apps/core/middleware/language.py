from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation


class DomainLocaleMiddleware(object):
    """
    Set language regarding of domain
    """
    def process_request(self, request):
        if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
            # Totally ignore the browser settings... 
            del request.META['HTTP_ACCEPT_LANGUAGE']

        current_domain = request.META['HTTP_HOST']
        lang_code = settings.LANGUAGES_DOMAINS[current_domain]
        translation.activate(lang_code)
        request.LANGUAGE_CODE = lang_code
