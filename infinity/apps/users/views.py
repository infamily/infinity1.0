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
        following = self.get_object().following
        following_user = following.all()
        context['ideas'] = [x.user_ideas.filter() for x in following_user]
        context['plans'] = [x.user_plans for x in following_user]
        context['steps'] = [x.user_steps for x in following_user]
        context['tasks'] = [x.user_tasks for x in following_user]
        context['works'] = [x.user_works for x in following_user]
        context['needs'] = [x.user_needs for x in following_user]
        context['goals'] = [x.user_goals for x in following_user]
        return context


class UserCryptsyNotificationToken(View):
    def get(self, request, *args, **kwargs):
        content = json.dumps({
            'result': True
        })
        return HttpResponse(content, content_type='application/liquid')


class UserDetailView(DetailView):

    """User detail view"""
    model = User
    slug_field = "username"
    template_name = "account/detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = kwargs.get('object')
        context['idea_list'] = user.user_ideas.all()
        context['plan_list'] = user.user_plans.all()
        context['step_list'] = user.user_steps.all()
        context['task_list'] = user.user_tasks.all()
        context['work_list'] = user.user_works.all()
        context['need_list'] = user.user_needs.all()
        context['goal_list'] = user.user_goals.all()

        context['guest_follow_me'] = self.request.user.get_relationships().filter(pk=user.pk)
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
