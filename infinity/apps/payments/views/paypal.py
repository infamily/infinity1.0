from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from ..systems import PayPal
from ..systems import PayPalException
from ..models import PayPalTransaction
from ..forms import PayPalTransactionForm

from users.decorators import ForbiddenUser
from core.models import Comment


User = get_user_model()


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class PayPalTransactionView(FormView):
    template_name = 'paypal/transaction/create.html'
    form_class = PayPalTransactionForm

    def dispatch(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        self.comment_model = get_object_or_404(Comment, pk=comment_id)
        if self.comment_model.user == self.request.user:
            # Adding Transactions to Comment should only be possible
            # only by the comment owner.
            return super(PayPalTransactionView, self).dispatch(
                request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

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

        try:
            paypal = PayPal(
                returnUrl=returnUrl,
                currency=currency
            )
        except PayPalException as e:
            messages.error(self.request, e)
            return super(PayPalTransactionView, self).form_invalid(form)

        try:
            user = User.objects.get(
                username=form.cleaned_data.get('recipient_username')
            )
        except User.DoesNotExist:
            messages.add_message(
                self.request,
                messages.ERROR,
                'User does not exist'
            )
            return super(PayPalTransactionView, self).form_invalid(form)

        result = paypal.adaptive_payment(
            comment_object=self.comment_model,
            receiver_amount=form.cleaned_data.get('amount'),
            receiver_user=user,
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
