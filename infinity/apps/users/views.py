import json
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import View
from django.views.generic import ListView
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages

from .forms import UserUpdateForm
from .models import User
from payments.decorators import ForbiddenUser


class FriendFollowingView(ListView):
    template_name = "account/friends/following.html"

    def get_queryset(self):
        qs = None
        return qs


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
