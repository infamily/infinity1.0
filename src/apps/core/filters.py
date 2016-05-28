from django import forms
from django.contrib.auth import get_user_model

import django_filters

from crispy_forms.helper import FormHelper

from crispy_forms.bootstrap import (
    FormActions,
    StrictButton,
    FieldWithButtons,
)

from crispy_forms.layout import (
    Layout,
    Fieldset,
    ButtonHolder,
    Submit,
    Field,
    HTML,
)

from .models import (
    Comment,
    Goal,
    Work,
    Idea,
    Step,
    Task,
    Definition,
    Type,
    Plan,
)

User = get_user_model()


class GoalListViewFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(GoalListViewFilter, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Goal

        fields = ['name']

        exclude = []


class WorkListViewFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(WorkListViewFilter, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Work

        fields = ['name']

        exclude = []


class IdeaListViewFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(IdeaListViewFilter, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Idea

        fields = ['name']


class StepListViewFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(StepListViewFilter, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Step

        fields = ['name']


class TaskListViewFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(TaskListViewFilter, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Task

        fields = ['name']

        exclude = []


class DefinitionLimitChoiceFilter(django_filters.Filter):
    field_class = forms.ChoiceField

    def filter(self, qs, value):
        if value:
            values = qs.values_list('pk')[:value]
            qs = qs.filter(pk__in=values)
            return qs
        values = qs.values_list('pk')[:100]
        qs = qs.filter(pk__in=values)
        return qs


class DefinitionListViewFilter(django_filters.FilterSet):
    OBJECTS_LIMITS = (
        (-1, 'ALL'),
        (100, '100'),
        (1000, '1000'),
        (10000, '10000'),
    )
    name = django_filters.CharFilter(lookup_type="icontains")
    number_of_definitions = DefinitionLimitChoiceFilter(choices=OBJECTS_LIMITS)

    @property
    def form(self):
        form = super(DefinitionListViewFilter, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.layout = Layout(
            FieldWithButtons(Field('name'), Submit('submit', 'Search', css_class='button white')),
            Field('number_of_definitions'),
        )

        return form

    class Meta:
        model = Definition

        fields = ['name']

        exclude = []


class PlanListViewFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(PlanListViewFilter, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Plan

        fields = ['name']

        exclude = []

