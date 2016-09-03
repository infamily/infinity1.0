from django.views.generic import FormView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from pure_pagination.mixins import PaginationMixin

from users.decorators import ForbiddenUser
from users.mixins import OwnerMixin
from payments.models import CoinAddress
from payments.forms import CoinAddressForm


class CoinAddressUpdateView(OwnerMixin, UpdateView):
    model = CoinAddress
    form_class = CoinAddressForm
    slug_field = "pk"
    template_name = "coin/update.html"

    def get_success_url(self):
        messages.success(self.request, _("Coin address succesfully updated"))
        return reverse("payments:coin_address_list")


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class CoinAddressCreateView(FormView):
    model = CoinAddress
    form_class = CoinAddressForm
    template_name = "coin/create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CoinAddressCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("CoinAddress succesfully created"))
        return reverse("payments:coin_address_list")


class CoinAddressDeleteView(OwnerMixin, DeleteView):
    model = CoinAddress
    slug_field = "pk"
    template_name = "coin/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("CoinAddress succesfully deleted"))
        return reverse("payments:coin_address_list")


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class CoinAddressListView(PaginationMixin, ListView):
    template_name = "coin/list.html"
    model = CoinAddress
    paginate_by = 10

    def get_queryset(self):
        qs = super(CoinAddressListView, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

