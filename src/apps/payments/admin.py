from django.contrib import admin

from .models import PayPalTransaction
from .models import CoinAddress


admin.site.register(PayPalTransaction)
admin.site.register(CoinAddress)
