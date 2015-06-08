from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field

from allauth.account.adapter import get_adapter
from allauth.account.forms import SignupForm as AllAuthSignupForm
from allauth.account.forms import LoginForm as AllAuthLoginForm

from core.models import (
    Comment,
    Goal,
    Work,
    Idea,
    Step,
    Task,
    User,
    Need,
    Type,
    Plan,
)


class CommentCreateFormDetail(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentCreateFormDetail, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Comment

        fields = [
            'task',
            'text',
            'work',
            'idea',
            'step',
            'plan',
        ]


class CommentCreateFormDetail(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentCreateFormDetail, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Comment

        fields = [
            'task',
            'goal',
            'text',
            'idea',
            'step',
            'plan',
        ]


class CommentCreateFormDetail(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentCreateFormDetail, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Comment

        fields = [
            'task',
            'goal',
            'text',
            'work',
            'step',
            'plan',
        ]


class CommentCreateFormDetail(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentCreateFormDetail, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Comment

        fields = [
            'task',
            'goal',
            'text',
            'work',
            'idea',
            'plan',
        ]


class CommentCreateFormDetail(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentCreateFormDetail, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Comment

        fields = [
            'goal',
            'text',
            'work',
            'idea',
            'step',
            'plan',
        ]


class CommentCreateFormDetail(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentCreateFormDetail, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Comment

        fields = [
            'task',
            'goal',
            'text',
            'work',
            'idea',
            'step',
            'plan',
        ]


class CommentCreateFormDetail(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentCreateFormDetail, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Comment

        fields = [
            'task',
            'goal',
            'text',
            'work',
            'idea',
            'step',
        ]


class CommentUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = Comment
        fields = [
            'goal',
            'text',
            'user',
            'idea',
            'plan',
            'step',
            'task',
            'work',
        ]


class CommentCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Comment
        exclude = [
            'created_at',
            'updated_at',
            'user',
        ]
        fields = [
            'idea',
            'text',
            'plan',
            'step',
            'task',
            'work',
            'goal',
        ]


class GoalCreateForm1(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GoalCreateForm1, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Goal
        exclude = [
            'need',
            'user',
        ]
        fields = [
            'name',
            'quantity',
            'reason',
            'personal',
        ]


class GoalUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GoalUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = Goal
        exclude = [
            'created_at',
            'user',
        ]
        fields = [
            'name',
            'quantity',
            'reason',
            'personal',
            'need',
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
        ]


class UserUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = User
        fields = [
            'email',
            'introduction',
        ]


class NeedCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NeedCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Need
        fields = [
            'type',
            'name',
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
        ]


class LoginForm(AllAuthLoginForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('login_form', _('Login')))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'


class SignUpUserForm(AllAuthSignupForm):

    email = forms.EmailField(
        max_length=150,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(SignUpUserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('signup_user_form', _('SignUp')))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_action = reverse('register') + '?user_type=user'
        self.helper.form_action += "&next=%s" % request.GET.get('next', '')

    def save(self, request):
        user = super(SignUpUserForm, self).save(request)
        setattr(user, 'email', self.cleaned_data.get('email'))
        user.save()
        return user
