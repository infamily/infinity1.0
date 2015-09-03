from django.utils.translation import ugettext as _
from django import forms

from django_select2.widgets import AutoHeavySelect2Widget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Submit, HTML, Layout, Fieldset, ButtonHolder
)

from core.models import Language
from .fields import MultipleEmailsField
from .fields import LanguageChoiceField


class InvitationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(InvitationForm, self).__init__(*args, **kwargs)

        self.fields['members_emails'] = MultipleEmailsField(
            widget=forms.TextInput(
                {
                    'placeholder': _('Enter one or more email addresses, '
                                     'separated by commas')
                }
            )
        )

        self.fields['email_body'] = forms.CharField(widget=forms.Textarea)
        self.fields['language'] = LanguageChoiceField(
            queryset=Language.objects.all(),
            widget=AutoHeavySelect2Widget
        )

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'members_emails',
                'language',
                'email_body',
                HTML("Invitations left: %s" % user.invitationoption.invitations_left),
                ButtonHolder(
                    Submit('submit', 'Send', css_class='button')
                )
            )
        )
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
