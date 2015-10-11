import json
from itertools import chain

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import redirect
from django.db.models.loading import get_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils import timezone

from pure_pagination.mixins import PaginationMixin
from braces.views import OrderableListMixin
from enhanced_cbv.views import ListFilteredView
from clever_selects.views import ChainedSelectChoicesView

from users.decorators import ForbiddenUser
from users.mixins import OwnerMixin
from users.forms import ConversationInviteForm
from .utils import CommentsContentTypeWrapper
from .utils import ViewTypeWrapper
from .utils import DetailViewWrapper
from .models import *
from .forms import *
from .filters import *

from hours.models import HourValue


class IndexView(TemplateView):
    template_name = 'home.html'
    dropdown_list = [0,2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('goals'):
            self.request.session['goals_number'] = int(self.request.POST['goals'])
        if self.request.POST.get('ideas'):
            self.request.session['ideas_number'] = int(self.request.POST['ideas'])
        if self.request.POST.get('plans'):
            self.request.session['plans_number'] = int(self.request.POST['plans'])
        if self.request.POST.get('steps'):
            self.request.session['steps_number'] = int(self.request.POST['steps'])
        if self.request.POST.get('tasks'):
            self.request.session['tasks_number'] = int(self.request.POST['tasks'])

        return redirect(reverse('home'))

    def get_context_data(self, **kwargs):
        items = {'goals': 64,
                 'ideas': 128,
                 'plans': 256,
                 'steps': 512,
                 'tasks': 1024}

        if self.request.session.get('goals_number'):
            items['goals'] = self.request.session['goals_number']
        if self.request.session.get('ideas_number'):
            items['ideas'] = self.request.session['ideas_number']
        if self.request.session.get('plans_number'):
            items['plans'] = self.request.session['plans_number']
        if self.request.session.get('steps_number'):
            items['steps'] = self.request.session['steps_number']
        if self.request.session.get('tasks_number'):
            items['tasks'] = self.request.session['tasks_number']

        now = timezone.now()
        in_days = lambda x: float(x.seconds/86400.)
        in_hours = lambda x: float(x.seconds/3600.)

        if self.request.user.is_authenticated():
            q_object = (
                Q(personal=False) |
                Q(personal=True, user=self.request.user) |
                Q(personal=True, sharewith=self.request.user)
            )
        else:
            q_object = Q(personal=False)

        goals = Goal.objects.filter(q_object).order_by('-commented_at')[:items['goals']]
        ideas = Idea.objects.filter(q_object).order_by('-commented_at')[:items['ideas']]
        plans = Plan.objects.filter(q_object).order_by('-commented_at')[:items['plans']]
        steps = Step.objects.filter(q_object).order_by('-commented_at')[:items['steps']]
        tasks = Task.objects.filter(q_object).order_by('-commented_at')[:items['tasks']]

        commented_at = lambda items: [obj.commented_at for obj in items]

        objects_list = list(chain(goals, ideas, plans, steps, tasks))
        dates = commented_at(objects_list)

        if dates:
            start = min(dates)
            days = in_days(now-start)
        else:
            start = timezone.now()
            days = 0.

        try:
            hour_value = HourValue.objects.latest('created_at')
        except HourValue.DoesNotExist:
            hour_value = 0

        context = {
            'goal_list': [(goal, goal.created_at > start) for goal in goals],
            'idea_list': [(idea, idea.created_at > start) for idea in ideas],
            'plan_list': [(plan, plan.created_at > start) for plan in plans],
            'step_list': [(step, step.created_at > start) for step in steps],
            'task_list': [(task, task.created_at > start) for task in tasks],
            'goal_hours': goals and 
                         '%0.2f' % in_hours(now-max(commented_at(list(goals))))
                         or 0.,
            'idea_hours': ideas and
                         '%0.2f' % in_hours(now-max(commented_at(list(ideas))))
                         or 0.,
            'plan_hours': plans and
                         '%0.2f' % in_hours(now-max(commented_at(list(plans))))
                         or 0,
            'step_hours': steps and
                         '%0.2f' % in_hours(now-max(commented_at(list(steps))))
                         or 0,
            'task_hours': tasks and
                         '%0.2f' % in_hours(now-max(commented_at(list(tasks))))
                         or 0,
            'last_days': '%0.2f' % days,
            'number_of_items': len(objects_list),
            'hour_value': hour_value,
            'dropdown_list': self.dropdown_list,
            'items': items,
        }

        context.update(kwargs)

        return context


class AjaxChainedView(ChainedSelectChoicesView):
    def get_choices(self):
        vals_list = []
        for x in range(1, 6):
            vals_list.append(x*int(self.parent_value))
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
class GoalCreateView(CreateView):

    """Goal create view"""
    model = Goal
    form_class = GoalCreateForm
    template_name = "goal/create1.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.need = form.cleaned_data.get('need')
        self.object.save()
        return super(GoalCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Goal succesfully created"))
        return reverse("goal-detail", args=[self.object.pk, ])

    def get_context_data(self, **kwargs):
        context = super(GoalCreateView, self).get_context_data(**kwargs)
        context.update({'need_object': self.need_instance})
        return context

    def dispatch(self, *args, **kwargs):
        if kwargs.get('need_id'):
            self.need_instance = get_object_or_404(Need, pk=int(kwargs['need_id']))
        else:
            self.need_instance = False
        return super(GoalCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(GoalCreateView, self).get_form_kwargs()
        kwargs['need_instance'] = self.need_instance
        return kwargs


class GoalListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name = "goal/list1.html"
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


class GoalDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

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

        conversation_form = ConversationInviteForm()
        next_url = "?next=%s" % self.request.path
        obj = kwargs.get('object')
        conversation_form.helper.form_action = reverse('user-conversation-invite', kwargs={
            'object_name': obj.__class__.__name__,
            'object_id': obj.id
        }) + next_url
        context.update({
            'conversation_form': conversation_form
        })

        return context


class GoalListView2(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name = "goal/list2.html"
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
class WorkListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name = "work/list1.html"
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
    template_name = "work/list2.html"
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


class WorkDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

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
        conversation_form = ConversationInviteForm()
        next_url = "?next=%s" % self.request.path
        obj = kwargs.get('object')
        conversation_form.helper.form_action = reverse('user-conversation-invite', kwargs={
            'object_name': obj.__class__.__name__,
            'object_id': obj.id
        }) + next_url
        context.update({
            'conversation_form': conversation_form
        })
        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class IdeaListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name = "idea/list1.html"
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
        messages.success(self.request, _("Idea succesfully created"))
        return reverse("idea-detail", args=[self.object.pk, ])

    def get_context_data(self, **kwargs):
        context = super(IdeaCreateView, self).get_context_data(**kwargs)
        context.update({'goal_object': self.goal_instance})
        return context

    def get_form_kwargs(self):
        kwargs = super(IdeaCreateView, self).get_form_kwargs()
        kwargs['goal_instance'] = self.goal_instance
        return kwargs


class IdeaDeleteView(OwnerMixin, DeleteView):

    """Idea delete view"""
    model = Idea
    slug_field = "pk"
    template_name = "idea/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Idea succesfully deleted"))
        return reverse('idea-list')


class IdeaListView2(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name = "idea/list2.html"
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


class IdeaDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

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

        conversation_form = ConversationInviteForm()
        next_url = "?next=%s" % self.request.path
        obj = kwargs.get('object')
        conversation_form.helper.form_action = reverse('user-conversation-invite', kwargs={
            'object_name': obj.__class__.__name__,
            'object_id': obj.id
        }) + next_url
        context.update({
            'conversation_form': conversation_form
        })
        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class StepListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):
    template_name = "step/list1.html"
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

    template_name = "step/list2.html"
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


class StepDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

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

        conversation_form = ConversationInviteForm()
        next_url = "?next=%s" % self.request.path
        obj = kwargs.get('object')
        conversation_form.helper.form_action = reverse('user-conversation-invite', kwargs={
            'object_name': obj.__class__.__name__,
            'object_id': obj.id
        }) + next_url
        context.update({
            'conversation_form': conversation_form
        })

        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class TaskListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name = "task/list1.html"
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


class TaskDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

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

        conversation_form = ConversationInviteForm()
        next_url = "?next=%s" % self.request.path
        obj = kwargs.get('object')
        conversation_form.helper.form_action = reverse('user-conversation-invite', kwargs={
            'object_name': obj.__class__.__name__,
            'object_id': obj.id
        }) + next_url
        context.update({
            'conversation_form': conversation_form
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
        if request.is_ajax():
            find_language = request.GET.get('find_language', None)
            if find_language:
                try:
                    language = Language.objects.get(
                        http_accept_language=find_language)
                except Language.DoesNotExist:
                    language = Language.objects.get(
                        pk=85)
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
            return redirect(reverse('goal-create', kwargs={'need_id': self.object.pk}))

        return render(request, 'need/create.html',
                      {'form': form})


class NeedListView(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name = "need/list.html"
    model = Need
    paginate_by = 10
    orderable_columns = ["created_at", "type", "name", ]
    orderable_columns_default = "-id"
    ordering = ["-id"]
    filter_set = NeedListViewFilter


class NeedDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

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
        conversation_form = ConversationInviteForm()
        next_url = "?next=%s" % self.request.path
        obj = kwargs.get('object')
        conversation_form.helper.form_action = reverse('user-conversation-invite', kwargs={
            'object_name': obj.__class__.__name__,
            'object_id': obj.id
        }) + next_url
        context.update({
            'conversation_form': conversation_form
        })
        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class PlanListView1(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name = "plan/list1.html"
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
        self.object.idea = form.cleaned_data.get('idea')
        self.object.save()
        return super(PlanCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Plan succesfully created"))
        return reverse("plan-detail", args=[self.object.pk, ])

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('idea_id'):
            self.idea_instance = get_object_or_404(Idea, pk=kwargs['idea_id'])
        else:
            self.idea_instance = False
        return super(PlanCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PlanCreateView, self).get_form_kwargs()
        kwargs['idea_instance'] = self.idea_instance
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PlanCreateView, self).get_context_data(**kwargs)
        context.update({'idea_object': self.idea_instance})
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

    template_name = "plan/list2.html"
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


class PlanDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

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

        conversation_form = ConversationInviteForm()
        next_url = "?next=%s" % self.request.path
        obj = kwargs.get('object')
        conversation_form.helper.form_action = reverse('user-conversation-invite', kwargs={
            'object_name': obj.__class__.__name__,
            'object_id': obj.id
        }) + next_url
        context.update({
            'conversation_form': conversation_form
        })

        return context

from core.forms import TranslationCreateForm


class TranslationCreateView(CreateView):
    model = Translation
    form_class = TranslationCreateForm
    template_name = 'translation/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.content_type_model = get_model(app_label='core', model_name=self.kwargs.get('model_name'))
        self.content_type = ContentType.objects.get_for_model(self.content_type_model)
        self.content_type_instance = self.content_type_model.objects.get(pk=kwargs.get('object_id'))

        return super(TranslationCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = "%s-detail" % self.kwargs.get('model_name')
        url = "%s?lang=%s" % (
            reverse(url, kwargs={'slug': self.content_type_instance.id}),
            self.object.language.language_code
        )
        return url

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.content_type = self.content_type
        self.object.object_id = self.content_type_instance.id
        self.object.save()

        return super(TranslationCreateView, self).form_valid(form)

    def get_form(self, form_class):
        form = super(TranslationCreateView, self).get_form(form_class)

        model_fields = [x.name for x in self.content_type_model._meta.fields]

        for field in form.fields:
            if field not in model_fields:
                form.fields.pop(field)

        return form
