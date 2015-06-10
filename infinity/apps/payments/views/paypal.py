from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from ..systems import PayPal
from ..models import PayPalTransaction
from ..forms import PayPalTransactionForm
from ..decorators import ForbiddenUser

from core.models import Comment


User = get_user_model()


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class PayPalTransactionView(FormView):
    template_name = 'paypal/transaction/create.html'
    form_class = PayPalTransactionForm

    def dispatch(self, request, *args, **kwargs):
        self.comment_model = get_object_or_404(Comment, pk=kwargs.get('comment_id'))
        return super(PayPalTransactionView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        current_site = get_current_site(self.request)
        returnUrl = "http://%s%s" % (
            current_site.domain,
            reverse('payments:transaction_paypal_success')
        )

        currency = int(self.request.POST.get('currency'))

        if currency == PayPalTransactionForm.USD:
            currency = 'USD'
        elif currency == PayPalTransactionForm.EUR:
            currency = 'EUR'

        paypal = PayPal(
            returnUrl=returnUrl,
            currency=currency
        )

        result = paypal.adaptive_payment(
            comment_id=self.comment_model,
            receiver_amount=form.cleaned_data.get('amount'),
            receiver_user=User.objects.get(
                email=form.cleaned_data.get('recipient_username')
            ),
            sender_user=self.request.user
        )

        self.payUrl = result['pay_url']
        return super(PayPalTransactionView, self).form_valid(form)

    def get_success_url(self):
        return self.payUrl


class PayPalTransactionSuccessView(View):
    def get(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        returnUrl = "http://%s%s" % (
            current_site.domain,
            reverse('payments:transaction_paypal_success')
        )
        paypal = PayPal(returnUrl=returnUrl)
        for transaction in PayPalTransaction.objects.filter(
                paymentExecStatus=PayPalTransaction.CREATED,
                sender_user=self.request.user
        ):
            paymentExecStatus = paypal.get_payment_information(
                transaction.payKey)['status'][0]

            if (paymentExecStatus != PayPalTransaction.CREATED and
                    transaction.paymentExecStatus == PayPalTransaction.CREATED):
                transaction.paymentExecStatus = paymentExecStatus

                transaction.save()
                return HttpResponse('success transaction')
        return HttpResponse('no transactions')
