from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_mail_template(
        subject_template_path,
        email_template_path,
        recipient_list,
        from_email=settings.DEFAULT_FROM_EMAIL,
        context={}):
    """
        Send email with template
    Args:
        subject_template_path(str): Subject
        email_template_path(str): Template Path
        recipient_list(list): 
        email_from(str): Email from with default argument from DEFAULT_EMAIL_FROM option
        context(dict): Django Template context
    """
    subject = render_to_string(subject_template_path, context)
    subject = ''.join(subject.splitlines())
    email = strip_tags(render_to_string(email_template_path, context))
    html_message = render_to_string(email_template_path, context)
    send_mail(subject, email, from_email, recipient_list, html_message=html_message)
