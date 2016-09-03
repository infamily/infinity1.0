from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import DeleteView

from pure_pagination.mixins import PaginationMixin
from braces.views import OrderableListMixin
from enhanced_cbv.views import ListFilteredView

from users.decorators import ForbiddenUser
from users.mixins import OwnerMixin
from users.forms import ConversationInviteForm

from ..forms import (
    TaskCreateForm,
    TaskUpdateForm,
)

from ..utils import (
    UpdateViewWrapper,
    DetailViewWrapper,
    ViewTypeWrapper,
    CommentsContentTypeWrapper,
    DeleteViewWrapper,
)

from ..models import (
    Step,
    Task,
    Work,
)

from ..utils import CreateViewWrapper
from ..filters import TaskListViewFilter


class TaskUpdateView(UpdateViewWrapper):

    """Task update view"""
    model = Task
    form_class = TaskUpdateForm
    slug_field = "pk"
    template_name = "task/update.html"

    def form_valid(self, form):
        return super(TaskUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Task succesfully updated"))
        return reverse("step-detail", args=[self.object.step.pk, ])


class TaskCreateView(CreateViewWrapper):

    """Task create view"""
    model = Task
    form_class = TaskCreateForm
    template_name = "task/create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.step = Step.objects.get(pk=self.kwargs['step'])
        self.object.save()
        return super(TaskCreateView, self).form_valid(form)

    def get_success_url(self):
        #messages.success(self.request, _("Task succesfully created"))
        return "%s?lang=%s" % (reverse("step-detail", args=[self.object.step.pk, ]), self.request.LANGUAGE_CODE)

    def get_context_data(self, **kwargs):
        context = super(TaskCreateView, self).get_context_data(**kwargs)
        context.update({
                    'step_object': Step.objects.get(pk=self.kwargs['step']),
        })
        return context

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['step_instance'] = Step.objects.get(pk=self.kwargs['step'])
        kwargs['request'] = self.request
        return kwargs


class TaskDeleteView(DeleteViewWrapper):

    """Task delete view"""
    model = Task
    slug_field = "pk"
    template_name = "task/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Task succesfully deleted"))
        return reverse("step-detail", args=[self.object.step.pk, ])


class TaskListView(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    """Task list view"""

    template_name = "task/list.html"

    model = Task
    paginate_by = 1000
    orderable_columns = [
        "name",
        "created_at",
        "updated_at",
        "priority",
        "step",
        "user",
    ]
    orderable_columns_default = "-id"
    filter_set = TaskListViewFilter


class TaskDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

    """Task detail view"""
    model = Task
    slug_field = "pk"
    template_name = "task/detail.html"

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)

        context.update({
            'work_list': Work.objects.filter(task=kwargs.get('object')).order_by('id')
        })

        return context
