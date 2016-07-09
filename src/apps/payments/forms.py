from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django import forms

import requests
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django_select2.forms import ModelSelect2Widget

from .models import CoinAddress
from users.models import User

from decimal import Decimal
from hours.models import HourValue


class CoinAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CoinAddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', _('Save')))

    class Meta:
        model = CoinAddress
        exclude = [
            'user'
        ]


class PayPalTransactionForm(forms.Form):
    recipient_username = forms.ModelChoiceField(queryset=User.objects.all())
    amount = forms.DecimalField()

    USD = 0
    EUR = 1

    CURRENCIES = (
        (USD, _("USD")),
        (EUR, _("EUR"))
    )

    currency = forms.ChoiceField(choices=CURRENCIES)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.comment_model = kwargs.pop('comment_model')
        super(PayPalTransactionForm, self).__init__(*args, **kwargs)
        self.fields['recipient_username'] = forms.ModelChoiceField(
            widget=ModelSelect2Widget(
                queryset=User.objects.all(),
                search_fields=['username__icontains']
            ),
            queryset=User.objects.all()
        )
        self.initial['recipient_username'] = self.comment_model.user.id

        self.initial['amount'] = max(Decimal(0), round((self.comment_model.hours_assumed+\
                                                        self.comment_model.hours_claimed-\
                                                        self.comment_model.hours_donated)*\
                                                       HourValue.objects.latest('created_at').value,2))
        self.fields['recipient_username'].label = _('Recipient username')
        self.fields['amount'].label = _('Amount')
        self.fields['currency'].label = _('Currency')

        if self.request.session.get('amount') and self.request.session.get('currency'):
            self.initial['amount'] = Decimal(self.request.session.get('amount'))
            self.initial['currency'] = int(self.request.session.get('currency'))
            del self.request.session['amount']
            del self.request.session['currency']

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('transaction_form', _('Invest'), css_class="btn-sm"))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'

