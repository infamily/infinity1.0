from itertools import chain
from urlparse import urljoin

from django.db.models import Q
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils import timezone
from django.utils import translation as trans_settings
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.views.generic import (
    FormView,
    TemplateView,
    RedirectView,
)

from users.decorators import ForbiddenUser
from users.models import User
from hours.models import HourValue
from core.models import Language

from ..forms import (
    ContentTypeSubscribeForm,
    SearchForm,
)

from ..models import (
    Translation,
    Need,
    Goal,
    Idea,
    Plan,
    Step,
    Task,
    Work,
)


class SetLanguageView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return urljoin('/', self.request.GET.get('next'))

    def get(self, request, *args, **kwargs):
        response = super(SetLanguageView, self).get(request, *args, **kwargs)
        lang = kwargs.get('lang')
        if lang:
            # To set the language for this session
            request.session[trans_settings.LANGUAGE_SESSION_KEY] = lang
            # To set it as a cookie
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang,
                                max_age=settings.LANGUAGE_COOKIE_AGE,
                                path=settings.LANGUAGE_COOKIE_PATH,
                                domain=settings.LANGUAGE_COOKIE_DOMAIN)
        return response


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class ContentTypeSubscribeFormView(FormView):
    """
    Subscribe/unsubscribe view
    """
    form_class = ContentTypeSubscribeForm
    template_name = "content_type_subscribe_form.html"

    def get_success_url(self):
        form = self.get_form()
        content_type_id = form.data.get('content_type')
        object_id = form.data.get('object_id')

        content_type = ContentType.objects.get(pk=content_type_id)

        return reverse("%s-detail" % content_type.model, kwargs={
            'slug': object_id
        })

    def form_valid(self, form):
        content_type = form.cleaned_data.get('content_type')
        object_id = form.cleaned_data.get('object_id')
        model = content_type.model_class()
        try:
            object_instance = model.objects.get(id=object_id)
        except model.DoesNotExist:
            messages.error(self.request, "Object with this id not found")
            return super(ContentTypeSubscribeFormView, self).form_invalid(form)

        if object_instance.subscribers.filter(pk=self.request.user.id):
            object_instance.subscribers.remove(self.request.user)
        else:
            object_instance.subscribers.add(self.request.user)

        object_instance.save()

        return super(ContentTypeSubscribeFormView, self).form_valid(form)


class LandingView(TemplateView):
    template_name = 'landing.html'
