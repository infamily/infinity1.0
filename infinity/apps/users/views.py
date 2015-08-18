import json
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import View
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from .forms import UserUpdateForm
from .models import User
from .decorators import ForbiddenUser


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
