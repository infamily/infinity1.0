import django_filters
import django_select2

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Reset

from core.models import (
    Comment,
    Transaction,
    Goal,
    Currency,
    Work,
    Idea,
    Platform,
    Step,
    Task,
    User,
    Address,
    Need,
    Type,
    Plan,
)


class CommentChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Comment.objects.all()
    search_fields = ['text__icontains', ]


class TransactionChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Transaction.objects.all()
    search_fields = ['transaction_external_id__icontains', ]


class GoalChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Goal.objects.all()
    search_fields = ['name__icontains', 'reason__icontains', ]


class CurrencyChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Currency.objects.all()
    search_fields = ['code__icontains', 'name__icontains']


class WorkChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Work.objects.all()
    search_fields = ['name__icontains', 'description__icontains']


class IdeaChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Idea.objects.all()
    search_fields = [
        'description__icontains',
        'name__icontains',
        'summary__icontains',
    ]


class PlatformChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Platform.objects.all()
    search_fields = ['name__icontains']


class StepChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Step.objects.all()
    search_fields = [
        'name__icontains',
        'deliverables__icontains',
        'objective__icontains',
        'investables__icontains']


class TaskChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Task.objects.all()
    search_fields = ['name__icontains', ]


class UserChoiceField(django_select2.AutoModelSelect2Field):
    queryset = User.objects.all()
    search_fields = ['introduction__icontains', ]


class AddressChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Address.objects.all()
    search_fields = ['address_external_id__icontains']


class NeedChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Need.objects.all()
    search_fields = ['name__icontains']


class TypeChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Type.objects.all()
    search_fields = ['name__icontains']


class PlanChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Plan.objects.all()
    search_fields = [
        'name__icontains',
        'deliverable__icontains',
        'situation__icontains']


class CommentChoiceFilter(django_filters.Filter):
    field_class = CommentChoiceField


class TransactionChoiceFilter(django_filters.Filter):
    field_class = TransactionChoiceField


class GoalChoiceFilter(django_filters.Filter):
    field_class = GoalChoiceField


class CurrencyChoiceFilter(django_filters.Filter):
    field_class = CurrencyChoiceField


class WorkChoiceFilter(django_filters.Filter):
    field_class = WorkChoiceField


class IdeaChoiceFilter(django_filters.Filter):
    field_class = IdeaChoiceField


class PlatformChoiceFilter(django_filters.Filter):
    field_class = PlatformChoiceField


class StepChoiceFilter(django_filters.Filter):
    field_class = StepChoiceField


class TaskChoiceFilter(django_filters.Filter):
    field_class = TaskChoiceField


class UserChoiceFilter(django_filters.Filter):
    field_class = UserChoiceField


class AddressChoiceFilter(django_filters.Filter):
    field_class = AddressChoiceField


class NeedChoiceFilter(django_filters.Filter):
    field_class = NeedChoiceField


class TypeChoiceFilter(django_filters.Filter):
    field_class = TypeChoiceField


class PlanChoiceFilter(django_filters.Filter):
    field_class = PlanChoiceField


class CommentListViewFilter1(django_filters.FilterSet):
    task = TaskChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Task'}))
    goal = GoalChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Goal'}))
    text = django_filters.CharFilter(lookup_type="icontains")
    work = WorkChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Work'}))
    idea = IdeaChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Idea'}))
    step = StepChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Step'}))
    plan = PlanChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Plan'}))

    @property
    def form(self):
        form = super(CommentListViewFilter1, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Comment

        fields = [
            u'goal',
            u'text',
            u'created_at',
            u'updated_at',
            u'idea',
            u'plan',
            u'step',
            u'task',
            u'work']

        exclude = []


class CommentListViewFilter2(django_filters.FilterSet):
    text = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(CommentListViewFilter2, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Comment

        fields = [u'text']

        exclude = []


class GoalListViewFilter1(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")
    reason = django_filters.CharFilter(lookup_type="icontains")
    user = UserChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'User'}))

    @property
    def form(self):
        form = super(GoalListViewFilter1, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Goal

        fields = [u'reason', u'name', u'quantity', u'user']

        exclude = []


class GoalListViewFilter2(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")
    reason = django_filters.CharFilter(lookup_type="icontains")
    user = UserChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'User'}))

    @property
    def form(self):
        form = super(GoalListViewFilter2, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Goal

        fields = [u'name', u'quantity', u'reason', u'personal', u'user']

        exclude = []


class WorkListViewFilter1(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")
    user = UserChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'User'}))
    description = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(WorkListViewFilter1, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Work

        fields = [u'name', u'description', u'url', u'parent_work_id', u'user']

        exclude = []


class WorkListViewFilter2(django_filters.FilterSet):
    task = TaskChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Task'}))
    name = django_filters.CharFilter(lookup_type="icontains")
    description = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(WorkListViewFilter2, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Work

        fields = [u'task', u'name', u'description']

        exclude = []


class IdeaListViewFilter1(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_type="icontains")
    name = django_filters.CharFilter(lookup_type="icontains")
    summary = django_filters.CharFilter(lookup_type="icontains")
    user = UserChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'User'}))

    @property
    def form(self):
        form = super(IdeaListViewFilter1, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Idea

        fields = [u'name', u'summary', u'description', u'user']

        exclude = []


class IdeaListViewFilter2(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_type="icontains")
    name = django_filters.CharFilter(lookup_type="icontains")
    summary = django_filters.CharFilter(lookup_type="icontains")
    goal = GoalChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Goal'}))

    @property
    def form(self):
        form = super(IdeaListViewFilter2, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Idea

        fields = [u'goal', u'name', u'summary', u'description']

        exclude = []


class StepListViewFilter1(django_filters.FilterSet):
    user = UserChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'User'}))
    name = django_filters.CharFilter(lookup_type="icontains")
    deliverables = django_filters.CharFilter(lookup_type="icontains")
    objective = django_filters.CharFilter(lookup_type="icontains")
    investables = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(StepListViewFilter1, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Step

        fields = [
            u'name',
            u'objective',
            u'deliverables',
            u'investables',
            u'priority',
            u'user']

        exclude = []


class StepListViewFilter2(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")
    deliverables = django_filters.CharFilter(lookup_type="icontains")
    plan = PlanChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Plan'}))
    objective = django_filters.CharFilter(lookup_type="icontains")
    investables = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(StepListViewFilter2, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Step

        fields = [
            u'plan',
            u'name',
            u'objective',
            u'investables',
            u'deliverables']

        exclude = []


class TaskListViewFilter1(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")
    user = UserChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'User'}))

    @property
    def form(self):
        form = super(TaskListViewFilter1, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Task

        fields = [u'name', u'priority', u'user']

        exclude = []


class TaskListViewFilter2(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")
    step = StepChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Step'}))

    @property
    def form(self):
        form = super(TaskListViewFilter2, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Task

        fields = [u'step', u'name']

        exclude = []


class NeedListViewFilter(django_filters.FilterSet):
    type = TypeChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Type'}))
    name = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(NeedListViewFilter, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Need

        fields = [u'type', u'name']

        exclude = []


class PlanListViewFilter1(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")
    deliverable = django_filters.CharFilter(lookup_type="icontains")
    user = UserChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'User'}))
    situation = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(PlanListViewFilter1, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Plan

        fields = [u'name', u'name', u'deliverable', u'situation', u'user']

        exclude = []


class PlanListViewFilter2(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")
    idea = IdeaChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Idea'}))
    deliverable = django_filters.CharFilter(lookup_type="icontains")
    situation = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(PlanListViewFilter2, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Plan

        fields = [u'name', u'idea', u'name', u'situation', u'deliverable']

        exclude = []


# Have to call it clearly to help django_select2 register fields
CommentChoiceField()
TransactionChoiceField()
GoalChoiceField()
CurrencyChoiceField()
WorkChoiceField()
IdeaChoiceField()
PlatformChoiceField()
StepChoiceField()
TaskChoiceField()
UserChoiceField()
AddressChoiceField()
NeedChoiceField()
TypeChoiceField()
PlanChoiceField()
