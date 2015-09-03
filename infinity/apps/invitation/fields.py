from django import forms
from django.core.validators import EmailValidator

from django_select2.fields import AutoModelSelect2Field


class LanguageChoiceField(AutoModelSelect2Field):
    search_fields = ['name__icontains']


class MultipleEmailsField(forms.Field):
    def clean(self, value):
        """
        Check that the field contains one or more comma-separated emails
        and normalizes the data to a list of the email strings.
        """
        if not value:
            raise forms.ValidationError('Enter at least one e-mail address separated by comma.')
        emails = [email.strip() for email in value.split(',')]
        email_validator = EmailValidator()
        for email in emails:
            email_validator(email)

        # Always return the cleaned data.
        return emails
