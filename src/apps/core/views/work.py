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

from ..utils import CreateViewWrapper

from ..forms import (
    WorkCreateForm,
    WorkUpdateForm,
)

from ..utils import (
    UpdateViewWrapper,
    DeleteViewWrapper,
    DetailViewWrapper,
    ViewTypeWrapper,
    CommentsContentTypeWrapper,
)

from ..models import (
    Task,
    Work,
)

from ..filters import WorkListViewFilter


class WorkUpdateView(UpdateViewWrapper):

    """Work update view"""
    model = Work
    form_class = WorkUpdateForm
    slug_field = "pk"
    template_name = "work/update.html"

    def form_valid(self, form):
        return super(WorkUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Work succesfully updated"))
        return reverse("work-detail", args=[self.object.pk, ])


class WorkCreateView(CreateViewWrapper):

    """Work create view"""
    model = Work
    form_class = WorkCreateForm
    template_name = "work/create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.task = Task.objects.get(pk=self.kwargs['task'])
        self.object.save()
        return super(WorkCreateView, self).form_valid(form)

    def get_success_url(self):
        #messages.success(self.request, _("Work succesfully created"))
        return "%s?lang=%s" % (reverse("work-detail", args=[self.object.pk, ]), self.object.language.language_code)

    def get_context_data(self, **kwargs):
        context = super(WorkCreateView, self).get_context_data(**kwargs)
        context.update({
            'task_object': Task.objects.get(pk=self.kwargs['task']),
        })
        return context

    def get_form_kwargs(self):
        kwargs = super(WorkCreateView, self).get_form_kwargs()
        kwargs['task_instance'] = Task.objects.get(pk=self.kwargs['task'])
        kwargs['request'] = self.request
        return kwargs


class WorkDeleteView(DeleteViewWrapper):

    """Work delete view"""
    model = Work
    slug_field = "pk"
    template_name = "work/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Work succesfully deleted"))
        return reverse("task-detail", args=[self.object.task.pk, ])


class WorkListView(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name = "work/list.html"
    model = Work
    paginate_by = 1000
    orderable_columns = [
        "task",
        "name",
        "url",
        "created_at",
        "updated_at",
        "user",
        "file",
        "parent_work_id",
        "description",
    ]
    orderable_columns_default = "-id"
    filter_set = WorkListViewFilter


class WorkDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

    """Work detail view"""
    model = Work
    slug_field = "pk"
    template_name = "work/detail.html"

    def get_context_data(self, **kwargs):
        context = super(WorkDetailView, self).get_context_data(**kwargs)

        context.update({
            'work_list': Work.objects.filter(parent_work_id=kwargs.get('object').id).order_by('-id')
        })

        return context
