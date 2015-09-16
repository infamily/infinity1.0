import json

from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.template import Context, Template
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import View
from django.views.generic import FormView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django import forms

from allauth.account.models import EmailAddress
from constance import config

from .forms import UserUpdateForm
from .forms import ConversationInviteForm
from .models import User
from .decorators import ForbiddenUser
from .models import ConversationInvite


class ConversationInviteView(FormView):
    form_class = ConversationInviteForm
    template_name = "account/invite.html"

    def get_form_kwargs(self):
        kwargs = super(ConversationInviteView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)

        try:
            email_exists = EmailAddress.objects.get(email=form.cleaned_data.get('email'))
        except EmailAddress.DoesNotExist:
            email_exists = False

        try:
            user_exists = User.objects.get(username=form.cleaned_data.get('name'))
        except User.DoesNotExist:
            user_exists = False

        if email_exists:
            form.add_error('email', forms.ValidationError(_('User with this email already exists')))
            return super(ConversationInviteView, self).form_invalid(form)

        if user_exists:
            form.add_error('name', forms.ValidationError(_('User with this name already exists')))
            return super(ConversationInviteView, self).form_invalid(form)

        user = User.objects.create(username=form.cleaned_data.get('name'))
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()

        EmailAddress.objects.create(
            user=user,
            email=form.cleaned_data.get('email'),
            verified=True
        )

        self.object.redirect_url = self.request.build_absolute_uri()
        self.object.user = user
        self.object.save()

        ctx = {
            'user_password': password,
            'user': user,
            'conversation_url': self.object.get_conversation_url()
        }

        template = Template(config.CONVERSATION_EMAIL_TEMPLATE)
        context = Context(ctx)
        subject = config.CONVERSATION_SUBJECT
        from_email = config.CONVERSATION_FROM_EMAIL
        message = template.render(context)

        EmailMessage(
            subject,
            message,
            to=[form.cleaned_data.get('email')],
            from_email=from_email
        ).send()

        return super(ConversationInviteView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        try:
            conversation_invite = ConversationInvite.objects.get(
                token=kwargs.get('token'),
                expired=False
            )
            user = conversation_invite.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect(conversation_invite.redirect_url)
        except ConversationInvite.DoesNotExist:
            return redirect(reverse('account_login'))


class FollowView(View):
    """ Follow/unfollow view
    """
    def post(self, request, *args, **kwargs):
        destination_user_id = int(request.POST.get('destination_user_id'))
        destination_user = User.objects.get(pk=destination_user_id)
        if request.user.get_relationships().filter(pk=destination_user_id).exists():
            request.user.remove_relationship(destination_user)
        else:
            request.user.add_relationship(destination_user)
        return redirect(reverse('user-detail', kwargs={'slug': destination_user.username}))


class FriendFollowingView(DetailView):
    template_name = "account/friends/following.html"
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super(FriendFollowingView, self).get_context_data(**kwargs)

        following_user = self.get_object()
        user = self.request.user
        if user.is_authenticated():
            if user.have_relationship_with(self.get_object()):
                context['ideas'] = following_user.user_ideas.all()
                context['plans'] = following_user.user_plans.all()
                context['steps'] = following_user.user_steps.all()
                context['tasks'] = following_user.user_tasks.all()
                context['goals'] = following_user.user_goals.all()
            else:
                context['ideas'] = following_user.user_ideas.filter(personal=False)
                context['plans'] = following_user.user_plans.filter(personal=False)
                context['steps'] = following_user.user_steps.filter(personal=False)
                context['tasks'] = following_user.user_tasks.filter(personal=False)
                context['goals'] = following_user.user_goals.filter(personal=False)
        else:
            context['ideas'] = following_user.user_ideas.filter(personal=False)
            context['plans'] = following_user.user_plans.filter(personal=False)
            context['steps'] = following_user.user_steps.filter(personal=False)
            context['tasks'] = following_user.user_tasks.filter(personal=False)
            context['goals'] = following_user.user_goals.filter(personal=False)

        return context


class UserCryptsyNotificationToken(View):
    def get(self, request, *args, **kwargs):
        content = json.dumps({
            'result': True
        })
        return HttpResponse(content, content_type='application/json')


class UserDetailView(DetailView):

    """User detail view"""
    model = User
    slug_field = "username"
    template_name = "account/detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = kwargs.get('object')
        if not user.is_superuser:
            context['idea_list'] = user.user_ideas.all()
            context['plan_list'] = user.user_plans.all()
            context['step_list'] = user.user_steps.all()
            context['task_list'] = user.user_tasks.all()
            context['work_list'] = user.user_works.all()
            context['need_list'] = user.user_needs.all()
            context['goal_list'] = user.user_goals.all()

        if self.request.user.is_authenticated():
            context['guest_follow_me'] = self.request.user.get_relationships(
            ).filter(pk=user.pk).exists()
        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class UserUpdateView(UpdateView):

    """User update view"""
    model = User
    form_class = UserUpdateForm
    slug_field = "pk"
    template_name = "account/update.html"

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get_success_url(self):
        messages.success(self.request, _("User succesfully updated"))
        return reverse("user-detail", kwargs={'slug': self.request.user.username})
