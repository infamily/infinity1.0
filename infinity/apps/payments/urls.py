from django.conf.urls import patterns, url

from .views import *


urlpatterns = patterns(
    '',
    url(
        r'^paypal/(?P<comment_id>\d+)/$',
        PayPalTransactionView.as_view(),
        name='transaction_paypal'
    ),
    url(
        r'^paypal/success/$',
        PayPalTransactionSuccessView.as_view(),
        name='transaction_paypal_success'
    ),
    url(
        r'^cryptsy/(?P<comment_id>\d+)/$',
        CryptsyTransactionView.as_view(),
        name='transaction_cryptsy'
    ),
    url(
        r'^cryptsy/credential/create/$',
        CryptsyCredentialCreateView.as_view(),
        name='cryptsy_credential_create'
    ),
    url(
        r'^cryptsy/credential/update/(?P<pk>\d+)/$',
        CryptsyCredentialUpdateView.as_view(),
        name='cryptsy_credential_update'
    ),
    url(
        r'^cryptsy/credential/list/$',
        CryptsyCredentialListView.as_view(),
        name='cryptsy_credential_list'
    ),
    url(
        r'^cryptsy/credential/delete/(?P<pk>\d+)/$',
        CryptsyCredentialDeleteView.as_view(),
        name='cryptsy_credential_delete'
    )
)
