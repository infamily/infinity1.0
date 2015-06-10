from django.shortcuts import render
from allauth.account.utils import complete_signup
from allauth.account.app_settings import EMAIL_VERIFICATION
from ..forms import LoginForm
from ..forms import SignUpUserForm


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
