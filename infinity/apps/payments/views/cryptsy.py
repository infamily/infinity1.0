from django.views.generic import FormView
from ..forms import CryptsyTransactionForm
from ..systems import CryptsyPay
from django.contrib import messages
from django.core.urlresolvers import reverse


class CryptsyTransactionView(FormView):
    form_class = CryptsyTransactionForm
    template_name = 'cryptsy-transaction.html'

    def form_valid(self, form):
        address_from = form.cleaned_data.get('address_from')
        address_to = form.cleaned_data.get('address_to')
        amount = form.cleaned_data.get('amount')
        currency = form.cleaned_data.get('currency')
        cryptsy = CryptsyPay(publickey=address_from)
        response = cryptsy.make_payment(
            address=address_to,
            amount=amount,
            currency_id=currency
        )
        if response["success"]:
            messages.add_message(
                self.request,
                messages.INFO,
                response["data"]["withdraw_id"]
            )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                response["error"][0]
            )
        return super(CryptsyTransactionView, self).form_valid(form)

    def get_success_url(self):
        return reverse('payments:transaction_cryptsy')

    def get_form_kwargs(self):
        kwargs = super(CryptsyTransactionView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
