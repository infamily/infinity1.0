from django.conf.urls import patterns, url

from .views import *


urlpatterns = patterns(
    '',
    url(
        r'^transaction/(?P<article_id>\d+)/$',
        PayPalTransactionView.as_view(),
        name='transaction_create'
    ),
    url(
        r'^transaction/success/$',
        PayPalTransactionSuccessView.as_view(),
        name='transaction_success'
    ),
    url(
        r'^transaction/cryptsy/$',
        CryptsyTransactionView.as_view(),
        name='transaction_cryptsy'
    )
)
