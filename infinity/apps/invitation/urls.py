
from django.conf.urls import patterns, url

from invitation.views import *


urlpatterns = patterns(
    '',
    url(
        '^$',
        InvitationFormView.as_view(),
        name="send"
    ),
    url(
        r'^token/(?P<token>.*)/$',
        InviteView.as_view(),
        name="token"
    ),
    url(
        r'^letter/detail/(?P<slug>\d+)/$',
        InvitationLetterTemplateView.as_view(),
        name="letter-detail"
    )
)
