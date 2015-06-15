from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from django.contrib import messages

from allauth.account.utils import complete_signup
from allauth.account.app_settings import EMAIL_VERIFICATION

from .forms import LoginForm
from .forms import UserUpdateForm
from .forms import SignUpUserForm
from .models import User
from .decorators import ForbiddenUser


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class UserDetailView(DetailView):

    """User detail view"""
    model = User
    slug_field = "pk"
    template_name = "user/detail.html"

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class UserUpdateView(UpdateView):

    """User update view"""
    model = User
    form_class = UserUpdateForm
    slug_field = "pk"
    template_name = "user/update.html"

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get_success_url(self):
        messages.success(self.request, _("User succesfully updated"))
        return reverse("user-detail", args=[])


def login(request):
    login_form = LoginForm()

    redirect_url = '/'
    redirect_url = request.GET.get('next') or redirect_url

    if request.method == 'POST' and 'login_form' in request.POST:
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            return login_form.login(request, redirect_url=redirect_url)

    return render(request, "user/login.html", {
        "login_form": login_form,
    })


def register(request):
    signup_form_user = SignUpUserForm(prefix="user", request=request)

    redirect_url = '/'
    redirect_url = request.GET.get('next') or redirect_url

    if request.method == 'POST' and 'signup_user_form' in request.POST:
        signup_form_user = SignUpUserForm(
            request.POST,
            prefix="user",
            request=request)

        if signup_form_user.is_valid():
            user = signup_form_user.save(request)
            return complete_signup(
                request,
                user,
                EMAIL_VERIFICATION,
                redirect_url)

    return render(request, "user/register.html", {
        "signup_form_user": signup_form_user,
    })
