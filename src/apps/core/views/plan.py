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

from ..utils import CreateViewWrapper
from ..forms import PlanCreateForm
from ..forms import PlanUpdateForm
from ..utils import UpdateViewWrapper
from ..utils import DetailViewWrapper
from ..utils import ViewTypeWrapper
from ..utils import CommentsContentTypeWrapper
from ..filters import PlanListViewFilter1
from ..filters import PlanListViewFilter2
from ..models import Plan
from ..models import Idea
from ..models import Step

from ..utils import get_plandf_dict
from ..utils import JsonView

import json
import stepio


class AjaxPlanStepsGraphDataView(JsonView):
    """
    Steps Graph Data View
    """
    def post(self, request, *args, **kwargs):
        username = self.request.GET.get('user', None)
        if username:
            steps = Step.objects.filter(plan__id=request.POST['id'], user__username=username).order_by('priority')
        else:
            steps = Step.objects.filter(plan__id=request.POST['id'], included=True).order_by('priority')
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


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
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
        messages.success(self.request, _("Plan succesfully created"))
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


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class PlanDeleteView(OwnerMixin, DeleteView):

    """Plan delete view"""
    model = Plan
    slug_field = "pk"
    template_name = "plan/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Plan succesfully deleted"))
        return reverse("idea-detail", args=[self.object.idea.pk, ])


class PlanListView2(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name = "plan/list2.html"
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
    filter_set = PlanListViewFilter2


class PlanDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

    """Plan detail view"""
    model = Plan
    slug_field = "pk"
    template_name = "plan/detail.html"

    def get_context_data(self, **kwargs):
        context = super(PlanDetailView, self).get_context_data(**kwargs)
        
        username = self.request.GET.get('user', None)
        if username:
            steps = Step.objects.filter(plan=kwargs.get('object'), user__username=username).order_by('priority')
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

        context.update({
            'step_list': steps,
            'plan_json': json.dumps(get_plandf_dict(plan_tuples))
        })

        return context
