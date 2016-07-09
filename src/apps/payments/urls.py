from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from .views import *


urlpatterns = [
    url(
        r'^paypal/list/$',
        PayPalTransactionListView.as_view(),
        name='transaction_paypal_list_view'
    ),
    url(
        r'^paypal/(?P<comment_id>\d+)/$',
        staff_member_required(
            PayPalTransactionView.as_view(),
        ),
        name='transaction_paypal'
    ),
    url(
        r'^paypal/success/$',
        PayPalTransactionSuccessView.as_view(),
        name='transaction_paypal_success'
    ),
    url(
        r'^coin/address/list/$',
        CoinAddressListView.as_view(),
        name='coin_address_list'
    ),
    url(
        r'^coin/address/create/$',
        CoinAddressCreateView.as_view(),
        name='coin_address_create'
    ),
    url(
        r'coin/address/update/(?P<slug>\d+)/$',
        CoinAddressUpdateView.as_view(),
        name='coin_address_update'
    ),
    url(
        r'coin/address/delete/(?P<slug>\d+)/$',
        CoinAddressDeleteView.as_view(),
        name='coin_address_delete'
    ),
]
