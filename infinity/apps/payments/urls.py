from django.conf.urls import patterns, url

from .views import *


urlpatterns = patterns(
    '',
    url(
        r'^transaction/paypal/(?P<ct_name>\w+)/(?P<obj_id>\d+)/$',
        PayPalTransactionView.as_view(),
        name='transaction_paypal'
    ),
    url(
        r'^transaction/paypal/success/$',
        PayPalTransactionSuccessView.as_view(),
        name='transaction_paypal_success'
    ),
    url(
        r'^transaction/cryptsy/(?P<ct_name>\w+)/(?P<obj_id>\d+)/$',
        CryptsyTransactionView.as_view(),
        name='transaction_cryptsy'
    )
)
