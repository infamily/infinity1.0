from django.utils.translation import ugettext as _
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from pure_pagination.mixins import PaginationMixin
from braces.views import OrderableListMixin
from enhanced_cbv.views import ListFilteredView

from users.decorators import ForbiddenUser
from .utils import CommentsContentTypeWrapper
from .utils import ViewTypeWrapper
from .models import *
from .forms import *
from .filters import *


class CommentListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name_list = "comment/list1.html"
    template_name_blocks = "comment/blocks1.html"
    model = Comment
    paginate_by = 10
    orderable_columns = [
        "task",
        "goal",
        "text",
        "created_at",
        "work",
        "updated_at",
        "idea",
        "step",
        "user",
        "plan",
    ]
    orderable_columns_default = "-id"
    filter_set = CommentListViewFilter1

    def get_base_queryset(self):
        queryset = super(CommentListView1, self).get_base_queryset()
        queryset = queryset.filter(user=self.request.user.pk)
        return queryset


class CommentUpdateView(UpdateView):

    """Comment update view"""
    model = Comment
    form_class = CommentUpdateForm
    slug_field = "pk"
    template_name = "comment/update.html"

    def get_success_url(self):
        messages.success(self.request, _("Comment succesfully updated"))
        return "/"


class CommentDeleteView(DeleteView):

    """Comment delete view"""
    model = Comment
    slug_field = "pk"
    template_name = "comment/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Comment succesfully deleted"))
        return "/"


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class CommentListView2(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    """Comment list view"""

    template_name_list = "comment/list2.html"
    template_name_blocks = "comment/blocks2.html"
    template_name = "comment/list2.html"

    model = Comment
    paginate_by = 10
    orderable_columns = [
        "task",
        "goal",
        "text",
        "created_at",
        "work",
        "updated_at",
        "idea",
        "step",
        "user",
        "plan",
    ]
    orderable_columns_default = "-id"
    filter_set = CommentListViewFilter2

    def get_base_queryset(self):
        queryset = super(CommentListView2, self).get_base_queryset()
        queryset = queryset.filter(goal__pk=self.kwargs['goal'])
        return queryset


class CommentCreateView(CreateView):

    """Comment create view"""
    model = Comment
    form_class = CommentCreateForm
    template_name = "comment/create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Comment succesfully created"))
        return "/"


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class GoalCreateView1(CreateView):

    """Goal create view"""
    model = Goal
    form_class = GoalCreateForm1
    template_name = "goal/create1.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.need = Need.objects.get(pk=self.kwargs['need'])
        self.object.save()
        return super(GoalCreateView1, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Goal succesfully created"))
        return reverse("goal-detail", args=[self.object.pk, ])


class GoalListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name_list = "goal/list1.html"
    template_name_blocks = "goal/blocks1.html"
    model = Goal
    paginate_by = 10
    orderable_columns = [
        "name",
        "personal",
        "created_at",
        "updated_at",
        "reason",
        "user",
        "need",
        "quantity",
    ]
    orderable_columns_default = "-id"
    filter_set = GoalListViewFilter1

    def get_base_queryset(self):
        queryset = super(GoalListView1, self).get_base_queryset()
        queryset = queryset.filter(need__pk=self.kwargs['need'])
        return queryset


class GoalDeleteView(DeleteView):

    """Goal delete view"""
    model = Goal
    slug_field = "pk"
    template_name = "goal/delete.html"

    def get_object(self, queryset=None):
        obj = super(GoalDeleteView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can delete Goal")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Goal succesfully deleted"))
        return reverse("goal-list1", args=[self.object.need.pk, ])


class GoalUpdateView(UpdateView):

    """Goal update view"""
    model = Goal
    form_class = GoalUpdateForm
    slug_field = "pk"
    template_name = "goal/update.html"

    def get_object(self, queryset=None):
        obj = super(GoalUpdateView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can update Goal")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(GoalUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Goal succesfully updated"))
        return reverse("goal-list1", args=[self.object.need.pk, ])


class GoalDetailView(DetailView, CommentsContentTypeWrapper):

    """Goal detail view"""
    model = Goal
    slug_field = "pk"
    template_name = "goal/detail.html"

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(GoalDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context


class GoalListView2(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name_list = "goal/list2.html"
    template_name_blocks = "goal/blocks2.html"
    model = Goal
    paginate_by = 10
    orderable_columns = [
        "name",
        "personal",
        "created_at",
        "updated_at",
        "reason",
        "user",
        "need",
        "quantity",
    ]
    orderable_columns_default = "-id"
    filter_set = GoalListViewFilter2


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class GoalCreateView2(CreateView):

    """Goal create view"""
    model = Goal
    form_class = GoalCreateForm2
    template_name = "goal/create2.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.need = Need.objects.get(pk=self.kwargs['need'])
        self.object.save()
        return super(GoalCreateView2, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Goal succesfully created"))
        return "/"


class WorkListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name_list = "work/list1.html"
    template_name_blocks = "work/blocks1.html"
    model = Work
    paginate_by = 10
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
    filter_set = WorkListViewFilter1

    def get_base_queryset(self):
        queryset = super(WorkListView1, self).get_base_queryset()
        queryset = queryset.filter(task__pk=self.kwargs['task'])
        return queryset


class WorkUpdateView(UpdateView):

    """Work update view"""
    model = Work
    form_class = WorkUpdateForm
    slug_field = "pk"
    template_name = "work/update.html"

    def get_object(self, queryset=None):
        obj = super(WorkUpdateView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can update Work")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(WorkUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Work succesfully updated"))
        return reverse("work-list1", args=[self.object.task.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class WorkCreateView(CreateView):

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
        messages.success(self.request, _("Work succesfully created"))
        return reverse("work-detail", args=[self.object.pk, ])


class WorkDeleteView(DeleteView):

    """Work delete view"""
    model = Work
    slug_field = "pk"
    template_name = "work-delete.html"

    def get_object(self, queryset=None):
        obj = super(WorkDeleteView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can delete Work")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Work succesfully deleted"))
        return reverse("work-list1", args=[self.object.task.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class WorkListView2(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name_list = "work/list2.html"
    template_name_blocks = "work/blocks2.html"
    model = Work
    paginate_by = 10
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
    filter_set = WorkListViewFilter2


class WorkDetailView(DetailView, CommentsContentTypeWrapper):

    """Work detail view"""
    model = Work
    slug_field = "pk"
    template_name = "work/detail.html"

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(WorkDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context


class IdeaListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name_list = "idea/list1.html"
    template_name_blocks = "idea/blocks1.html"
    model = Idea
    paginate_by = 10
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
    filter_set = IdeaListViewFilter1

    def get_base_queryset(self):
        queryset = super(IdeaListView1, self).get_base_queryset()
        queryset = queryset.filter(goal__pk=self.kwargs['goal'])
        return queryset


class IdeaUpdateView(UpdateView):

    """Idea update view"""
    model = Idea
    form_class = IdeaUpdateForm
    slug_field = "pk"
    template_name = "idea/update.html"

    def get_object(self, queryset=None):
        obj = super(IdeaUpdateView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can update Idea")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(IdeaUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Idea succesfully updated"))
        return reverse("idea-list1", args=[self.object.goal.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class IdeaCreateView(CreateView):

    """Idea create view"""
    model = Idea
    form_class = IdeaCreateForm
    template_name = "idea/create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.goal = Goal.objects.get(pk=self.kwargs['goal'])
        self.object.save()
        return super(IdeaCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Idea succesfully created"))
        return reverse("idea-detail", args=[self.object.pk, ])


class IdeaDeleteView(DeleteView):

    """Idea delete view"""
    model = Idea
    slug_field = "pk"
    template_name = "idea/delete.html"

    def get_object(self, queryset=None):
        obj = super(IdeaDeleteView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can delete Idea")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Idea succesfully deleted"))
        return reverse("idea-list1", args=[self.object.goal.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class IdeaListView2(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name_list = "idea/list2.html"
    template_name_blocks = "idea/blocks2.html"
    model = Idea
    paginate_by = 10
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
    filter_set = IdeaListViewFilter2


class IdeaDetailView(DetailView, CommentsContentTypeWrapper):

    """Idea detail view"""
    model = Idea
    slug_field = "pk"
    template_name = "idea/detail.html"

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(IdeaDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context


class StepListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name_list = "step/list1.html"
    template_name_blocks = "step/blocks1.html"
    model = Step
    paginate_by = 10
    orderable_columns = [
        "user",
        "name",
        "created_at",
        "updated_at",
        "deliverables",
        "priority",
        "plan",
        "objective",
        "investables",
    ]
    orderable_columns_default = "-id"
    filter_set = StepListViewFilter1

    def get_base_queryset(self):
        queryset = super(StepListView1, self).get_base_queryset()
        queryset = queryset.filter(plan__pk=self.kwargs['plan'])
        return queryset


class StepUpdateView(UpdateView):

    """Step update view"""
    model = Step
    form_class = StepUpdateForm
    slug_field = "pk"
    template_name = "step/update.html"

    def get_object(self, queryset=None):
        obj = super(StepUpdateView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can update Step")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(StepUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Step succesfully updated"))
        return reverse("step-list1", args=[self.object.plan.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class StepCreateView(CreateView):

    """Step create view"""
    model = Step
    form_class = StepCreateForm
    template_name = "step/create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.plan = Plan.objects.get(pk=self.kwargs['plan'])
        self.object.save()
        return super(StepCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Step succesfully created"))
        return reverse("step-detail", args=[self.object.pk, ])


class StepDeleteView(DeleteView):

    """Step delete view"""
    model = Step
    slug_field = "pk"
    template_name = "step/delete.html"

    def get_object(self, queryset=None):
        obj = super(StepDeleteView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can delete Step")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Step succesfully deleted"))
        return reverse("step-list1", args=[self.object.plan.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class StepListView2(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name_list = "step/list2.html"
    template_name_blocks = "step/blocks2.html"
    model = Step
    paginate_by = 10
    orderable_columns = [
        "user",
        "name",
        "created_at",
        "updated_at",
        "deliverables",
        "priority",
        "plan",
        "objective",
        "investables",
    ]
    orderable_columns_default = "-id"
    filter_set = StepListViewFilter2

    def get_base_queryset(self):
        queryset = super(StepListView2, self).get_base_queryset()
        queryset = queryset.filter(user=self.request.user.pk)
        return queryset


class StepDetailView(DetailView, CommentsContentTypeWrapper):

    """Step detail view"""
    model = Step
    slug_field = "pk"
    template_name = "step/detail.html"

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(StepDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context


class TaskListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name_list = "task/list1.html"
    template_name_blocks = "task/blocks1.html"
    model = Task
    paginate_by = 10
    orderable_columns = [
        "name",
        "created_at",
        "updated_at",
        "priority",
        "step",
        "user",
    ]
    orderable_columns_default = "-id"
    filter_set = TaskListViewFilter1

    def get_base_queryset(self):
        queryset = super(TaskListView1, self).get_base_queryset()
        queryset = queryset.filter(step__pk=self.kwargs['step'])
        return queryset


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class TaskUpdateView(UpdateView):

    """Task update view"""
    model = Task
    form_class = TaskUpdateForm
    slug_field = "pk"
    template_name = "task/update.html"

    def get_object(self, queryset=None):
        obj = super(TaskUpdateView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can update Task")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TaskUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Task succesfully updated"))
        return reverse("task-list1", args=[self.object.step.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class TaskCreateView(CreateView):

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
        messages.success(self.request, _("Task succesfully created"))
        return reverse("task-detail", args=[self.object.pk, ])


class TaskDeleteView(DeleteView):

    """Task delete view"""
    model = Task
    slug_field = "pk"
    template_name = "task/delete.html"

    def get_object(self, queryset=None):
        obj = super(TaskDeleteView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can delete Task")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Task succesfully deleted"))
        return reverse("task-list1", args=[self.object.step.pk, ])


class TaskListView2(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    """Task list view"""

    template_name = "task/list2.html"
    template_name_list = "task/list2.html"
    template_name_blocks = "task/blocks2.html"

    model = Task
    paginate_by = 10
    orderable_columns = [
        "name",
        "created_at",
        "updated_at",
        "priority",
        "step",
        "user",
    ]
    orderable_columns_default = "-id"
    filter_set = TaskListViewFilter2


class TaskDetailView(DetailView, CommentsContentTypeWrapper):

    """Task detail view"""
    model = Task
    slug_field = "pk"
    template_name = "task/detail.html"

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class NeedCreateView(CreateView):

    """Need create view"""
    model = Need
    form_class = NeedCreateForm
    template_name = "need/create.html"

    def get_success_url(self):
        messages.success(self.request, _("Need succesfully created"))
        return reverse("goal-create1", args=[self.object.pk, ])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(NeedCreateView, self).form_valid(form)


class NeedListView(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name_list = "need/list.html"
    template_name_blocks = "need/blocks.html"
    model = Need
    paginate_by = 10
    orderable_columns = ["created_at", "type", "name", ]
    orderable_columns_default = "-id"
    filter_set = NeedListViewFilter


class NeedDetailView(DetailView, CommentsContentTypeWrapper):

    """Need detail view"""
    model = Need
    slug_field = "pk"
    template_name = "need/detail.html"

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(NeedDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context


class PlanListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name_list = "plan/list1.html"
    template_name_blocks = "plan/blocks1.html"
    model = Plan
    paginate_by = 10
    orderable_columns = [
        "name",
        "created_at",
        "updated_at",
        "idea",
        "deliverable",
        "user",
        "situation",
    ]
    orderable_columns_default = "-id"
    filter_set = PlanListViewFilter1

    def get_base_queryset(self):
        queryset = super(PlanListView1, self).get_base_queryset()
        queryset = queryset.filter(idea__pk=self.kwargs['idea'])
        return queryset


class PlanUpdateView(UpdateView):

    """Plan update view"""
    model = Plan
    form_class = PlanUpdateForm
    slug_field = "pk"
    template_name = "plan/update.html"

    def get_object(self, queryset=None):
        obj = super(PlanUpdateView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can update Plan")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(PlanUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Plan succesfully updated"))
        return reverse("plan-list1", args=[self.object.idea.pk, ])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class PlanCreateView(CreateView):

    """Plan create view"""
    model = Plan
    form_class = PlanCreateForm
    template_name = "plan/create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.idea = Idea.objects.get(pk=self.kwargs['idea'])
        self.object.save()
        return super(PlanCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Plan succesfully created"))
        return reverse("plan-detail", args=[self.object.pk, ])


class PlanDeleteView(DeleteView):

    """Plan delete view"""
    model = Plan
    slug_field = "pk"
    template_name = "plan/delete.html"

    def get_object(self, queryset=None):
        obj = super(PlanDeleteView, self).get_object(queryset)
        if obj.user.pk != self.request.user.pk:
            raise Http404("Only owner can delete Plan")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Plan succesfully deleted"))
        return reverse("plan-list1", args=[self.object.idea.pk, ])


class PlanListView2(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name_list = "plan/list2.html"
    template_name_blocks = "plan/blocks2.html"
    model = Plan
    paginate_by = 10
    orderable_columns = [
        "name",
        "created_at",
        "updated_at",
        "idea",
        "deliverable",
        "user",
        "situation",
    ]
    orderable_columns_default = "-id"
    filter_set = PlanListViewFilter2


class PlanDetailView(DetailView, CommentsContentTypeWrapper):

    """Plan detail view"""
    model = Plan
    slug_field = "pk"
    template_name = "plan/detail.html"

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(PlanDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = None
        if self.request.user.__class__.__name__ not in [u'AnonymousUser']:
            form = self.get_form_class()
        context.update({
            'form': form,
        })
        context.update({
            'object_list': self.object_list,
        })
        return context


