from django.views.generic import FormView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

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

    def post(self, request, *args, **kwargs):
        user_credential = self.request.user.credential
        # Set all credentials to False
        user_credential.filter(default=True).update(default=False)

        # Set the obtained by id credential "default" field in False
        credential_id = int(request.POST.get('credential_id'))
        credential = user_credential.get(id=credential_id)
        credential.default = True
        credential.save()

        # Redirect to the current page
        return redirect(reverse("payments:cryptsy_credential_list"))

    def get_queryset(self):
        qs = super(CryptsyCredentialListView, self).get_queryset()

        qs = qs.filter(user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super(CryptsyCredentialListView, self).get_context_data(**kwargs)
        context['current_domain'] = Site.objects.get_current().domain
        return context

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
        # from django import forms
        # form.add_error('notificationtoken', forms.ValidationError('asd'))
        # return super(CryptsyCredentialCreateView, self).form_invalid(form)
        form_object = form.save(commit=False)
        form_object.user = self.request.user
        current_site = Site.objects.get_current()
        form_object.save()
        form_object.notificationtoken = 'http://%s%s' % (
            current_site.domain, reverse('cryptsy_notification_token', kwargs={
                'username': self.request.user.username,
                'credential_id': form_object.id
            })
        )
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
        self.comment_id = kwargs.get('comment_id')
        self.comment_model = get_object_or_404(Comment, pk=self.comment_id)
        cryptsy_credential = request.user.credential.filter(default=True)
        if not cryptsy_credential.exists():
            messages.add_message(self.request, messages.INFO, _('You have not added any credential. Please create a Credential or select default'))
            return redirect(reverse('payments:cryptsy_credential_list'))
        else:
            cryptsy_credential = request.user.credential.get(default=True)
            self.cryptsy_publickey = cryptsy_credential.publickey
        return super(CryptsyTransactionView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        address_to = form.cleaned_data.get('address_to')
        amount = form.cleaned_data.get('amount')
        currency = form.cleaned_data.get('currency')
        cryptsy = CryptsyPay(publickey=self.cryptsy_publickey)
        response = cryptsy.make_payment(
            comment_object=self.comment_model,
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
        return reverse('payments:transaction_cryptsy', kwargs={'comment_id': self.comment_id})

    def get_form_kwargs(self):
        kwargs = super(CryptsyTransactionView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
