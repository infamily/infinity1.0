from django.utils.translation import ugettext_lazy as _
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div


from core.models import Comment
from core.models import Goal
from core.models import Work
from core.models import Idea
from core.models import Step
from core.models import Task
from core.models import Need
from core.models import Plan
from core.models import Language


class CommentCreateFormDetail(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentCreateFormDetail, self).__init__(*args, **kwargs)

        self.fields['text'].label = _('Comment')
        self.fields['notify'].label = _('Notify mentioned users by e-mail.')
        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Comment
        fields = [
            'text',
            'notify'
        ]


class CommentUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = _('Comment')
        self.fields['notify'].label = _('Notify mentioned users by e-mail.')

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = Comment
        fields = [
            'text',
            'notify'
        ]


class CommentCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentCreateForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = _('Comment')
        self.fields['notify'].label = _('Notify mentioned users by e-mail.')

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Comment
        exclude = [
            'created_at',
            'updated_at',
            'user',
        ]


class GoalCreateForm1(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GoalCreateForm1, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

        self.fields['name'].label = _('<b>Description:</b> (used in title, e.g., "Our community in Nepal needs water this summer.")')
        self.fields['quantity'].label = _('<b>Quantity:</b> (appears next to Goal title, e.g., 50000)')
        self.fields['unit'].label = _('<b>Unit:</b> (appears next to quantity, e.g., "liters")')
        self.fields['reason'].label = _('<b>Reason:</b> (appears after the title, write full description here)')
        self.fields['personal'].label = _('<b>Personal</b> (makes the entry visible only to your friends)')


    class Meta:
        model = Goal
        exclude = [
            'need',
            'user',
        ]
        fields = [
            'name',
            'quantity',
            'unit',
            'reason',
            'personal',
        ]


class GoalUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GoalUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

        self.fields['name'].label = 'Description'

    class Meta:
        model = Goal
        exclude = [
            'created_at',
            'user',
        ]
        fields = [
            'name',
            'quantity',
            'unit',
            'reason',
            'personal',
        ]


class GoalCreateForm2(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GoalCreateForm2, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Goal
        exclude = [
            'created_at',
            'updated_at',
            'need',
            'user',
        ]
        fields = [
            'name',
            'quantity',
            'unit',
            'reason',
            'personal',
        ]


class WorkUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WorkUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = Work
        exclude = [
            'created_at',
            'user',
        ]
        fields = [
            'name',
            'file',
            'description',
            'url',
            'parent_work_id',
            'task',
            'personal'
        ]


class WorkCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WorkCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Work
        exclude = [
            'task',
            'user',
        ]
        fields = [
            'name',
            'description',
            'url',
            'file',
            'parent_work_id',
            'personal'
        ]


class IdeaUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(IdeaUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = Idea
        exclude = [
            'created_at',
            'user',
        ]
        fields = [
            'name',
            'summary',
            'description',
            'goal',
            'personal'
        ]


class IdeaCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(IdeaCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Idea
        exclude = [
            'created_at',
            'goal',
            'user',
        ]
        fields = [
            'name',
            'summary',
            'description',
            'personal'
        ]


class StepUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StepUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = Step
        exclude = [
            'created_at',
            'updated_at',
            'user',
        ]
        fields = [
            'name',
            'objective',
            'priority',
            'investables',
            'deliverables',
            'plan',
            'personal'
        ]


class StepCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StepCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Step
        exclude = [
            'plan',
            'updated_at',
            'created_at',
            'user',
        ]
        fields = [
            'name',
            'objective',
            'priority',
            'investables',
            'deliverables',
            'personal'
        ]


class TaskUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = Task
        exclude = [
            'created_at',
            'updated_at',
            'user',
        ]
        fields = [
            'name',
            'priority',
            'step',
            'personal'
        ]


class TaskCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Task
        exclude = [
            'step',
            'created_at',
            'updated_at',
            'user',
        ]
        fields = [
            'name',
            'priority',
            'personal'
        ]


class NeedCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NeedCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Div(
                Div('language', css_class='col-sm-2',),
                Div(
                    Field('name', placeholder=kwargs.pop('query_placeholder',
                                                         'Name')),
                    css_class='col-sm-10',
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Div(
                        Field(
                            'definition', placeholder=kwargs.pop('query_placeholder', 'Type your own definition'),
                            # type="hidden",
                        ),
                        css_class='col-sm-10',
                    ),
                    Div(
                        Field(Submit('submit', _('Add & Go'))),
                        # css_class='col-sm-2 hidden create-button',
                        css_class='col-sm-2 create-button',
                    ),
                    css_class='col-sm-12 hints-block',
                ),
                css_class='row'
            ),
        )
        self.fields['name'].label = ''
        self.fields['language'].label = ''
        self.fields['definition'].label = ''

    class Meta:
        model = Need
        fields = [
            'name',
            'language',
            'definition',
        ]


class NeedUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NeedUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = Need
        fields = [
            'name',
            'language',
            'definition',
        ]


class PlanUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PlanUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = Plan
        exclude = [
            'created_at',
            'updated_at',
            'user',
        ]
        fields = [
            'name',
            'situation',
            'deliverable',
            'name',
            'idea',
            'personal'
        ]


class PlanCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PlanCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Plan
        exclude = [
            'idea',
            'user',
        ]
        fields = [
            'name',
            'situation',
            'deliverable',
            'name',
            'personal'
        ]


