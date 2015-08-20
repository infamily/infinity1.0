import json

from django.utils.translation import ugettext as _
import json
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.detail import BaseDetailView
from django.shortcuts import redirect

from pure_pagination.mixins import PaginationMixin
from braces.views import OrderableListMixin
from enhanced_cbv.views import ListFilteredView

from users.decorators import ForbiddenUser
from users.mixins import OwnerMixin

from .utils import CommentsContentTypeWrapper
from .utils import ViewTypeWrapper
from .models import *
from .forms import *
from .filters import *

from clever_selects.views import ChainedSelectChoicesView

class AjaxChainedView(ChainedSelectChoicesView):
    def get_choices(self):
        vals_list = []
        for x in range(1, 6):
            vals_list.append(x*int(self.parent_value))
        result = tuple(zip(vals_list, vals_list))
        address = User.objects.get(pk=self.parent_value).address.all()
        res = tuple(
            zip(
                [x.pk for x in address],
                ['(%s) %s' % (x.currency_code, x.address) for x in address]
            )
        )
        return res


class CommentListView1(PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name = "comment/list1.html"
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


class CommentUpdateView(OwnerMixin, UpdateView):

    """Comment update view"""
    model = Comment
    form_class = CommentUpdateForm
    slug_field = "pk"
    template_name = "comment/update.html"

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        messages.success(self.request, _("Comment succesfully updated"))
        if next_url:
            return next_url
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
class CommentListView2(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Comment list view"""

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

    def get_context_data(self, **kwargs):
        context = super(GoalCreateView1, self).get_context_data(**kwargs)
        context.update({
                    'need_object': Need.objects.get(pk=self.kwargs['need']),
        })
        return context


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
        "unit",
    ]
    orderable_columns_default = "-id"
    filter_set = GoalListViewFilter1


class GoalDeleteView(OwnerMixin, DeleteView):

    """Goal delete view"""
    model = Goal
    slug_field = "pk"
    template_name = "goal/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Goal succesfully deleted"))
        return reverse("need-detail", args=[self.object.need.pk, ])


class GoalUpdateView(OwnerMixin, UpdateView):

    """Goal update view"""
    model = Goal
    form_class = GoalUpdateForm
    slug_field = "pk"
    template_name = "goal/update.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(GoalUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Goal succesfully updated"))
        return reverse("goal-detail", args=[self.object.pk, ])


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
        context.update({
            'idea_list': Idea.objects.filter(goal=kwargs.get('object')).order_by('-id')
        })
        return context


class GoalListView2(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name_list = "goal/list2.html"
    template_name_blocks = "goal/blocks2.html"
    model = Goal
    paginate_by = 10
    orderable_columns = [
        "id",
    ]
    orderable_columns_default = "-id"
    filter_set = GoalListViewFilter2

    # def get_base_queryset(self):
    #     queryset = super(GoalListView2, self).get_base_queryset()
    #     queryset = queryset.filter(need=self.kwargs.get('need'))
    #     return queryset


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


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
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


class WorkUpdateView(OwnerMixin, UpdateView):

    """Work update view"""
    model = Work
    form_class = WorkUpdateForm
    slug_field = "pk"
    template_name = "work/update.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(WorkUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Work succesfully updated"))
        return reverse("work-detail", args=[self.object.pk, ])


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

    def get_context_data(self, **kwargs):
        context = super(WorkCreateView, self).get_context_data(**kwargs)
        context.update({
                    'task_object': Task.objects.get(pk=self.kwargs['task']),
        })
        return context


class WorkDeleteView(OwnerMixin, DeleteView):

    """Work delete view"""
    model = Work
    slug_field = "pk"
    template_name = "work/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Work succesfully deleted"))
        return reverse("work-list1", args=[self.object.task.pk, ])


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
        context.update({
            'work_list': Work.objects.filter(parent_work_id=kwargs.get('object').id).order_by('-id')
        })
        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
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


class IdeaUpdateView(OwnerMixin, UpdateView):

    """Idea update view"""
    model = Idea
    form_class = IdeaUpdateForm
    slug_field = "pk"
    template_name = "idea/update.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(IdeaUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Idea succesfully updated"))
        return reverse("idea-detail", args=[self.object.pk, ])


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

    def get_context_data(self, **kwargs):
        context = super(IdeaCreateView, self).get_context_data(**kwargs)
        context.update({
                    'goal_object': Goal.objects.get(pk=self.kwargs['goal']),
        })
        return context


class IdeaDeleteView(OwnerMixin, DeleteView):

    """Idea delete view"""
    model = Idea
    slug_field = "pk"
    template_name = "idea/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Idea succesfully deleted"))
        return reverse("idea-list1", args=[self.object.goal.pk, ])


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
        context.update({
            'plan_list': Plan.objects.filter(idea=kwargs.get('object')).order_by('-id')
        })
        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
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


class StepUpdateView(OwnerMixin, UpdateView):

    """Step update view"""
    model = Step
    form_class = StepUpdateForm
    slug_field = "pk"
    template_name = "step/update.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(StepUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Step succesfully updated"))
        return reverse("plan-detail", args=[self.object.plan.pk, ])


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
        return reverse("plan-detail", args=[self.object.plan.pk, ])

    def get_context_data(self, **kwargs):
        context = super(StepCreateView, self).get_context_data(**kwargs)
        context.update({
                    'plan_object': Plan.objects.get(pk=self.kwargs['plan']),
        })
        return context


class StepDeleteView(OwnerMixin, DeleteView):

    """Step delete view"""
    model = Step
    slug_field = "pk"
    template_name = "step/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Step succesfully deleted"))
        return reverse("step-list1", args=[self.object.plan.pk, ])


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
        context.update({
            'task_list': Task.objects.filter(step=kwargs.get('object')).order_by('id')
        })
        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
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


class TaskUpdateView(OwnerMixin, UpdateView):

    """Task update view"""
    model = Task
    form_class = TaskUpdateForm
    slug_field = "pk"
    template_name = "task/update.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TaskUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Task succesfully updated"))
        return reverse("step-detail", args=[self.object.step.pk, ])


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
        return reverse("step-detail", args=[self.object.step.pk, ])

    def get_context_data(self, **kwargs):
        context = super(TaskCreateView, self).get_context_data(**kwargs)
        context.update({
                    'step_object': Step.objects.get(pk=self.kwargs['step']),
        })
        return context


class TaskDeleteView(OwnerMixin, DeleteView):

    """Task delete view"""
    model = Task
    slug_field = "pk"
    template_name = "task/delete.html"

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
        context.update({
            'work_list': Work.objects.filter(task=kwargs.get('object')).order_by('id')
        })
        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class NeedUpdateView(OwnerMixin, UpdateView):

    """Need update view"""
    model = Need
    form_class = NeedUpdateForm
    slug_field = "pk"
    template_name = "need/update.html"

    def dispatch(self, *args, **kwargs):
        owner = Need.objects.get(pk=self.kwargs['slug']).user
        if self.request.user != owner:
            return redirect(reverse('need-detail',
                                    kwargs={'slug': self.kwargs['slug']}))
        return super(NeedUpdateView, self).dispatch(*args, **kwargs)


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(NeedUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Need succesfully updated"))
        return reverse("need-detail", args=[self.object.pk, ])


class NeedCreateView(CreateView):

    """Need create view"""
    model = Need
    form_class = NeedCreateForm
    template_name = "need/create.html"

    def get(self, request, **kwargs):
        if self.request.user.__class__.__name__ == u'AnonymousUser':
            return render(request, 'about.html')
        if request.is_ajax():
            find_language = request.GET.get('find_language', None)
            if find_language:
                try:
                    language = Language.objects.get(
                        http_accept_language=find_language)
                except Language.DoesNotExist:
                    language = Language.objects.get(
                        name='English')
                return HttpResponse(language.pk)

            hints = []
            similar_needs = Need.objects.filter(
                language__pk=request.GET['language'],
                name=request.GET['name']
            )
            for need in similar_needs:
                if need.definition:
                    hints.append([need.definition,
                                  reverse('need-detail', args=[need.pk])])
            resp = json.dumps(hints)
            return HttpResponse(resp, content_type='application/json')
        form = NeedCreateForm()
        return render(request, 'need/create.html',
                      {'form': form})

    def post(self, request, **kwargs):
        form = NeedCreateForm(request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            messages.success(self.request, _("Need succesfully created"))
            return HttpResponseRedirect(reverse('need-list', args=[]))
        return render(request, 'need/create.html',
                      {'form': form})


class NeedListView(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name_list = "need/list.html"
    template_name_blocks = "need/blocks.html"
    model = Need
    paginate_by = 10
    orderable_columns = ["created_at", "type", "name", ]
    orderable_columns_default = "-id"
    ordering = ["-id"]
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
        context.update({
            'goal_list': Goal.objects.filter(need=kwargs.get('object')).order_by('-id')
        })
        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
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


class PlanUpdateView(OwnerMixin, UpdateView):

    """Plan update view"""
    model = Plan
    form_class = PlanUpdateForm
    slug_field = "pk"
    template_name = "plan/update.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(PlanUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Plan succesfully updated"))
        return reverse("plan-detail", args=[self.object.pk, ])


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

    def get_context_data(self, **kwargs):
        context = super(PlanCreateView, self).get_context_data(**kwargs)
        context.update({
                    'idea_object': Idea.objects.get(pk=self.kwargs['idea']),
        })
        return context


class PlanDeleteView(OwnerMixin, DeleteView):

    """Plan delete view"""
    model = Plan
    slug_field = "pk"
    template_name = "plan/delete.html"

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
        context.update({
            'step_list': Step.objects.filter(plan=kwargs.get('object')).order_by('id')
        })
        return context
