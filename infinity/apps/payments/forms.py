from django.utils.translation import ugettext_lazy as _
from django import forms

import requests
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import CryptsyCredential


class CryptsyTransactionForm(forms.Form):
    address_from = forms.ChoiceField()
    address_to = forms.CharField()
    amount = forms.DecimalField()
    currency = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CryptsyTransactionForm, self).__init__(*args, **kwargs)
        self.fields['address_from'].choices = [
            (x.publickey, x.publickey)
            for x in self.request.user.credential.all()
        ]
        response = requests.get('https://api.cryptsy.com/api/v2/currencies')

        self.fields['currency'].choices = [
            (currency['id'], currency['code'])
            for i, currency in enumerate(response.json()['data'])
        ]

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('transaction_form', _('Pay')))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'


class PayPalTransactionForm(forms.Form):
    recipient_username = forms.CharField()
    amount = forms.IntegerField()

    USD = 0
    EUR = 1

    CURRENCIES = (
        (USD, _("USD")),
        (EUR, _("EUR"))
    )

    currency = forms.ChoiceField(choices=CURRENCIES)

    def __init__(self, *args, **kwargs):
        super(PayPalTransactionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('transaction_form', _('Pay')))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'


class CryptsyCredentialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CryptsyCredentialForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('transaction_form', _('Save')))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'

    class Meta:
        model = CryptsyCredential
        exclude = ['user']
