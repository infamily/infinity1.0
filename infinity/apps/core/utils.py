from django.contrib.contenttypes.models import ContentType
from .forms import CommentCreateFormDetail
from .models import Comment
from django.views.generic import CreateView
from django.core.exceptions import FieldError

from django.template.loader import render_to_string
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

        url = "%s/%s/detail/#" % (comment_instance.content_type,
                                  comment_instance.content_object.id)
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
    send_mail(subject, email, from_email, recipient_list, html_message=None)


class ViewTypeWrapper(object):
    default_view_type = 'list'
    allowed_view_types = [u'list', u'blocks']

    def get_template_names(self):
        """
            Override standart method that return template name

            In view_type transferred the display type
            (value on the basis of which will be decided what kind
            of template to choose: a table, block or gallery).

            This value is stored in the session, and passed to a
            get_template_by_view_type method that returns template
            based on the transmitted view_type
        """

        view_type = self.get_view_type()

        return self.get_template_by_view_type(view_type)

    def get_view_type(self):
        """
        Returns view_type based on the get parameter from session.
        We record a view_type in session,
        if in the get parameter are passed new value

        In get paramater we get view type
        check whether there is a resulting string in the list of allowed view_type
        if the value of view_type correspondence list, then save this value
        back default view_type in session
        """
        view_type = self.request.GET.get('view_type')

        if view_type in self.allowed_view_types:
            self.request.session['view_type'] = view_type
            self.request.session.save()
            return view_type

        view_type = self.request.session.get('view_type')

        return view_type or self.default_view_type

    def get_template_by_view_type(self, view_type):
        """
            Return template name by view type

            :param view_type: on the basis
            of this parameter we define
            how to display the content

            view_type can receive three values: map, gallery, table.
            Depending on the view type.
            For example, if we give view_type value "table",
            then we display page as a table
        """

        if view_type not in self.allowed_view_types:
            view_type = self.default_view_type

        return getattr(self, 'template_name_%s' % view_type, None)

    def get_context_data(self, **kwargs):
        context = super(ViewTypeWrapper, self).get_context_data(**kwargs)
        context['allowed_view_types'] = self.allowed_view_types
        return context

    def get_base_queryset(self):
        """
        Show entries with personal = True for content owners only
        Show entries with personal = False for anonymous users
        """
        qs = super(ViewTypeWrapper, self).get_base_queryset()
        if self.request.user.is_anonymous():
            try:
                qs = qs.filter(personal=False)
            except FieldError:
                pass
        else:
            try:
                qs = (qs.filter(personal=False) |
                      qs.filter(personal=True, user=self.request.user))
            except FieldError:
                pass
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
