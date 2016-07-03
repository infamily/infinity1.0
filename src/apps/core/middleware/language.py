from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation


class DomainLocaleMiddleware(object):
    """
    Set language regarding of domain
    """
    def process_request(self, request):
        # TODO: looks weird, should be refactored later

        if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
            # Totally ignore the browser settings...
            del request.META['HTTP_ACCEPT_LANGUAGE']

        current_domain = request.META.get('HTTP_HOST')

        if current_domain:
            lang_code = settings.LANGUAGES_DOMAINS.get(current_domain)

            if lang_code:
                translation.activate(lang_code)
                request.LANGUAGE_CODE = lang_code
