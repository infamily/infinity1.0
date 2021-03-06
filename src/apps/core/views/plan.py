import json

from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import DeleteView

import stepio

from pure_pagination.mixins import PaginationMixin
from braces.views import OrderableListMixin
from enhanced_cbv.views import ListFilteredView

from users.decorators import ForbiddenUser
from users.mixins import OwnerMixin
from users.forms import ConversationInviteForm

from ..forms import (
    PlanCreateForm,
    PlanUpdateForm,
)

from ..utils import (
    UpdateViewWrapper,
    DetailViewWrapper,
    DeleteViewWrapper,
    ViewTypeWrapper,
    CommentsContentTypeWrapper,
    CommentsEngageContentTypeWrapper,
)


from ..models import (
    Plan,
    Idea,
    Step,
)

from ..utils import (
    get_plandf_dict,
    JsonView,
    CreateViewWrapper
)

from ..filters import PlanListViewFilter


class AjaxStepIncludeView(JsonView):
    """
    Steps Graph Data View
    """
    def post(self, request, *args, **kwargs):
        step_id = request.POST.get('step_id')
        step = Step.objects.get(id=step_id)
        if request.user in step.plan.members.all() or request.user == step.plan.user:
            if step.included:
                step.included = False
            else:
                step.included= True
            step.save()
        return self.json({'included': step.included, 'step_id': step_id})


class AjaxPlanStepsGraphDataView(JsonView):
    """
    Steps Graph Data View
    """
    def post(self, request, *args, **kwargs):
        username = self.request.GET.get('user', None)
        if username:
            steps = Step.objects.filter(plan__id=request.POST['id'], user__username=username).order_by('user_priority')
            print 'username: ', username
        else:
            steps = Step.objects.filter(plan__id=request.POST['id'], included=True).order_by('priority')
            print 'username: ', None
        #steps = Step.objects.filter(plan__id=request.POST['id']).order_by('priority')
        #plan_tuples = [(step.investables, step.deliverables) for step in steps]
        plan_tuples = []
        for step in steps:
            try:
                stepio.parse(step.investables)
                stepio.parse(step.deliverables)
                plan_tuples.append((step.investables, step.deliverables))
            except:
                """ skipping un-parse-able step """
                pass
        plan_dict = get_plandf_dict(plan_tuples)
        return self.json(plan_dict)


class PlanUpdateView(UpdateViewWrapper):

    """Plan update view"""
    model = Plan
    form_class = PlanUpdateForm
    slug_field = "pk"
    template_name = "plan/update.html"

    def form_valid(self, form):
        return super(PlanUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Plan succesfully updated"))
        return reverse("plan-detail", args=[self.object.pk, ])


class PlanCreateView(CreateViewWrapper):

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
        #messages.success(self.request, _("Plan succesfully created"))
        return "%s?lang=%s" % (reverse("plan-detail", args=[self.object.pk, ]), self.object.language.language_code)

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('idea_id'):
            self.idea_instance = get_object_or_404(Idea, pk=kwargs['idea_id'])
        else:
            self.idea_instance = False
        return super(PlanCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PlanCreateView, self).get_form_kwargs()
        kwargs['idea_instance'] = self.idea_instance
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PlanCreateView, self).get_context_data(**kwargs)
        context.update({'idea_object': self.idea_instance})
        return context


class PlanDeleteView(DeleteViewWrapper):

    """Plan delete view"""
    model = Plan
    slug_field = "pk"
    template_name = "plan/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Plan succesfully deleted"))
        return reverse("idea-detail", args=[self.object.idea.pk, ])


class PlanListView(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name = "plan/list.html"
    model = Plan
    paginate_by = 1000
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
    filter_set = PlanListViewFilter


class PlanDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

    """Plan detail view"""
    model = Plan
    slug_field = "pk"
    template_name = "plan/detail.html"

    def get_context_data(self, **kwargs):
        context = super(PlanDetailView, self).get_context_data(**kwargs)

        username = self.request.GET.get('user', None)
        if username:
            steps = Step.objects.filter(plan=kwargs.get('object'), user__username=username).order_by('user_priority')
        else:
            steps = Step.objects.filter(plan=kwargs.get('object'), included=True).order_by('priority')
        #plan_tuples = [(step.investables, step.deliverables) for step in steps]
        plan_tuples = []
        for step in steps:
            try:
                stepio.parse(step.investables)
                stepio.parse(step.deliverables)
                plan_tuples.append((step.investables, step.deliverables))
            except:
                """ skipping un-parse-able step """
                pass
        user_set = set([step.user for step in  Step.objects.filter(plan=kwargs.get('object'))])
        context.update({
            'step_list': steps,
            'plan_json': json.dumps(get_plandf_dict(plan_tuples)),
            'user_set': user_set
        })

        return context


class PlanEngageView(DetailViewWrapper, CommentsEngageContentTypeWrapper):

    """Plan engage view"""
    model = Plan
    slug_field = "pk"
    template_name = "plan/engage.html"

    def get_context_data(self, **kwargs):
        context = super(PlanEngageView, self).get_context_data(**kwargs)

        username = self.request.GET.get('user', None)
        if username:
            steps = Step.objects.filter(plan=kwargs.get('object'), user__username=username).order_by('user_priority')
        else:
            steps = Step.objects.filter(plan=kwargs.get('object'), included=True).order_by('priority')
        #plan_tuples = [(step.investables, step.deliverables) for step in steps]
        plan_tuples = []
        for step in steps:
            try:
                stepio.parse(step.investables)
                stepio.parse(step.deliverables)
                plan_tuples.append((step.investables, step.deliverables))
            except:
                """ skipping un-parse-able step """
                pass
        user_set = set([step.user for step in  Step.objects.filter(plan=kwargs.get('object'))])
        context.update({
            'step_list': steps,
            'plan_json': json.dumps(get_plandf_dict(plan_tuples)),
            'user_set': user_set
        })

        return context
