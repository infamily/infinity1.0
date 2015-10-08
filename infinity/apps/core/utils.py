from django.contrib.contenttypes.models import ContentType
from .forms import CommentCreateFormDetail
from .models import Comment
from django.views.generic import CreateView
from django.core.exceptions import FieldError

from django.template.loader import render_to_string
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from constance import config
from users.models import User
from os import path
from re import finditer


def notify_mentioned_users(comment_instance):
    """
    """
    comment = comment_instance.text
    usernames = [m.group(1) for m in finditer('\[([^]]+)\]', comment)]
    usernames = usernames[:config.MAX_MENTIONS_PER_COMMENT]
    subject_template_path = 'mail/comments/mention_notification_subject.txt'
    email_template_path = 'mail/comments/mention_notification.html'

    users = User.objects.filter(username__in=usernames)

    if users.exists():

        from .utils import send_mail_template
        from django.contrib.sites.models import Site

        url = "%s/%s/detail/#comment-%s" % (comment_instance.content_type,
                                  comment_instance.content_object.id,
                                  comment_instance.id)
        link = path.join(path.join('http://', Site.objects.get_current().domain), url)

        for user in users.iterator():
            send_mail_template(subject_template_path,
                               email_template_path,
                               recipient_list=[user.email],
                               context={'user': comment_instance.user.username,
                                        'comment': comment_instance.text,
                                        'link': link})


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


class ViewTypeWrapper(object):
    def get_base_queryset(self):
        qs = super(ViewTypeWrapper, self).get_base_queryset()
        if self.request.user.is_anonymous():
            # Show entries with personal = False for anonymous users
            qs = qs.filter(personal=False)
        else:
            # Conditions description
            # Show entries with personal = False
            # Show entries with personal = True for content owners only
            # Show entries with personal = True if content shared with current user
            qs = qs.filter(
                Q(personal=False) |
                Q(personal=True, user=self.request.user) |
                Q(personal=True, sharewith=self.request.user)
            )
        return qs


class CommentsContentTypeWrapper(CreateView):
    model_for_list = Comment

    form_class = CommentCreateFormDetail

    @property
    def object_list(self):
        content_type = ContentType.objects.get_for_model(
            self.get_object()
        )
        object_list = self.model_for_list.objects.filter(
            content_type__pk=content_type.pk,
            object_id=self.get_object().id
        )

        return object_list.order_by('id')

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.content_type = ContentType.objects.get_for_model(self.get_object())
        self.object.object_id = self.get_object().id
        self.object.save()
        notify_mentioned_users(self.object)
        return super(CommentsContentTypeWrapper, self).form_valid(form)
