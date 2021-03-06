from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import DeleteView

from pure_pagination.mixins import PaginationMixin
from braces.views import OrderableListMixin
from enhanced_cbv.views import ListFilteredView

from users.decorators import ForbiddenUser
from users.mixins import OwnerMixin
from users.forms import ConversationInviteForm

from ..utils import (
    CreateViewWrapper,
    ViewTypeWrapper,
    UpdateViewWrapper,
    DetailViewWrapper,
    CommentsContentTypeWrapper,
    DeleteViewWrapper,
)

from ..models import (
    Goal,
    Idea,
    Plan,
)

from ..forms import (
    IdeaUpdateForm,
    IdeaCreateForm
)

from ..filters import IdeaListViewFilter


class IdeaUpdateView(UpdateViewWrapper):

    """Idea update view"""
    model = Idea
    form_class = IdeaUpdateForm
    slug_field = "pk"
    template_name = "idea/update.html"

    def form_valid(self, form):
        return super(IdeaUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Idea succesfully updated"))
        return reverse("idea-detail", args=[self.object.pk, ])


class IdeaCreateView(CreateViewWrapper):

    """Idea create view"""
    model = Idea
    form_class = IdeaCreateForm
    template_name = "idea/create.html"

    def dispatch(self, *args, **kwargs):
        if kwargs.get('goal_id'):
            self.goal_instance = get_object_or_404(Goal, pk=kwargs['goal_id'])
        else:
            self.goal_instance = False
        return super(IdeaCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        for goal in form.cleaned_data.get('goal'):
            self.object.goal.add(goal)
        self.object.save()
        return super(IdeaCreateView, self).form_valid(form)

    def get_success_url(self):
        #messages.success(self.request, _("Idea succesfully created"))
        if self.object.personal:
            return reverse("inbox")
        else:
            return "%s?lang=%s" % (reverse("idea-detail", args=[self.object.pk, ]), self.object.language.language_code)

    def get_context_data(self, **kwargs):
        context = super(IdeaCreateView, self).get_context_data(**kwargs)
        context.update({'goal_object': self.goal_instance})
        return context

    def get_form_kwargs(self):
        kwargs = super(IdeaCreateView, self).get_form_kwargs()
        kwargs['goal_instance'] = self.goal_instance
        kwargs['request'] = self.request
        return kwargs


class IdeaDeleteView(DeleteViewWrapper):

    """Idea delete view"""
    model = Idea
    slug_field = "pk"
    template_name = "idea/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Idea succesfully deleted"))
        return reverse('inbox')


class IdeaListView(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name = "idea/list.html"
    model = Idea
    paginate_by = 1000
    orderable_columns = [
        "description",
        "name",
        "created_at",
        "updated_at",
        "summary",
        "user",
        "goal",
    ]
    orderable_columns_default = "-id"
    filter_set = IdeaListViewFilter


class IdeaDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

    """Idea detail view"""
    model = Idea
    slug_field = "pk"
    template_name = "idea/detail.html"

    def get_context_data(self, **kwargs):
        context = super(IdeaDetailView, self).get_context_data(**kwargs)

        context.update({
            'plan_list': Plan.objects.filter(idea=kwargs.get('object')).order_by('-id')
        })

        return context
