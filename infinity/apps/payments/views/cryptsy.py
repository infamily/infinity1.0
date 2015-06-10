from django.views.generic import FormView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404

from pure_pagination.mixins import PaginationMixin

from ..forms import CryptsyTransactionForm
from ..systems import CryptsyPay
from ..forms import CryptsyCredentialForm
from ..models import CryptsyCredential
from ..decorators import ForbiddenUser

from core.models import Comment


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class CryptsyCredentialUpdateView(UpdateView):
    form_class = CryptsyCredentialForm
    slug_field = 'pk'
    template_name = 'cryptsy/credential/update.html'
    model = CryptsyCredential

    def form_valid(self, form):
        form_object = form.save(commit=False)
        form_object.user = self.request.user
        form_object.save()
        return super(CryptsyCredentialUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Credential succesfully updated"))
        return reverse("payments:cryptsy_credential_list")


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class CryptsyCredentialListView(PaginationMixin, ListView):
    model = CryptsyCredential
    paginate_by = 10
    template_name = 'cryptsy/credential/list.html'

    def get_base_queryset(self):
        queryset = super(CryptsyCredentialListView, self).get_base_queryset()
        queryset = queryset.filter(user=self.request.user.pk)
        return queryset


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class CryptsyCredentialDeleteView(DeleteView):
    model = CryptsyCredential
    slug_field = 'pk'
    template_name = 'cryptsy/credential/delete.html'

    def get_success_url(self):
        messages.success(self.request, _("Credential succesfully deleted"))
        return reverse("payments:cryptsy_credential_list")


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class CryptsyCredentialCreateView(FormView):
    form_class = CryptsyCredentialForm
    template_name = 'cryptsy/credential/create.html'

    def form_valid(self, form):
        form_object = form.save(commit=False)
        form_object.user = self.request.user
        form_object.save()
        return super(CryptsyCredentialCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Credential succesfully created"))
        return reverse("payments:cryptsy_credential_list")


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class CryptsyTransactionView(FormView):
    form_class = CryptsyTransactionForm
    template_name = 'cryptsy/transaction/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.comment_model = get_object_or_404(Comment, pk=kwargs.get('comment_id'))
        return super(CryptsyTransactionView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        address_from = form.cleaned_data.get('address_from')
        address_to = form.cleaned_data.get('address_to')
        amount = form.cleaned_data.get('amount')
        currency = form.cleaned_data.get('currency')
        cryptsy = CryptsyPay(publickey=address_from)
        response = cryptsy.make_payment(
            comment=self.comment_model,
            address=address_to,
            amount=amount,
            currency_id=currency,
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
