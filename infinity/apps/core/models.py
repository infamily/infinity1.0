from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
#from django.db.models.signals import post_save

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

#from .signals import _comment_post_save

from django_markdown.models import MarkdownField

from djmoney_rates.utils import convert_money

from re import finditer
from decimal import Decimal
from hours.models import HourValue

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = MarkdownField(blank=False)
    notify = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        unique=False,
        null=False,
        blank=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
    )
    hours_donated = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_claimed = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_matched = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    def __unicode__(self):
        return u"Comment #%s" % self.id

    def get_absolute_url(self):
        return "/"

    def save(self, *args, **kwargs):
        "Save comment created date to parent object."
        self.sum_hours_claimed()
        self.match_hours()
        super(Comment, self).save(*args, **kwargs)
        self.content_object.commented_at = self.created_at
        self.content_object.save()
        self.content_object.sum_hours()

    def delete(self, *args, **kwargs):
        "Update comment created date for parent object."
        super(Comment, self).delete(*args, **kwargs)
        comments = Comment.objects.filter(object_id=self.object_id)
        if comments:
            self.content_object.commented_at = \
                comments.latest('created_at').created_at
        else:
            self.content_object.commented_at = \
                self.content_object.created_at
        self.content_object.save()

    def sum_hours_donated(self):
        self.hours_donated = sum([tx.hours for tx in self.paypal_transaction.all()])
        #+= sum([tx.amount for tx in self.cryptsy_transaction.all()])
        self.match_hours()
        self.save()

    def sum_hours_claimed(self):
        self.hours_claimed = Decimal(0.)
        for m in finditer('\{([^}]+)\}', self.text):
            try:
                hours = float(m.group(1))
                self.hours_claimed += Decimal(hours)
            except:
                pass

    def match_hours(self):
        if self.hours_claimed >= self.hours_donated:
            ratio = Decimal(1.)
        elif self.hours_claimed < self.hours_donated:
            ratio = self.hours_claimed/self.hours_donated

        self.hours_matched = Decimal(0.)
        for tx in self.paypal_transaction.all():
            tx.hours_matched = tx.hours * ratio
            self.hours_matched += tx.hours_matched

    def get_usd(self):
        return self.hours_donated*HourValue.objects.latest('created_at').value

class Goal(models.Model):
    type = models.ForeignKey(
        'Type',
        blank=False,
        null=False,
    )
    need = models.ForeignKey(
        'Need',
        blank=False,
        null=False,
    )
    name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )
    language = models.ForeignKey(
        'Language',
        blank=True,
        null=True,
    )
    personal = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        unique=False,
        null=False,
        blank=False,
    )
    commented_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    reason = MarkdownField(blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        related_name='user_goals'
    )
    hours_donated = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_claimed = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_matched = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"

    def sum_hours(self):
        self.hours_donated = Decimal(0.)
        self.hours_claimed = Decimal(0.)
        self.hours_matched = Decimal(0.)
        for comment in Comment.objects.filter(content_type__pk=\
            ContentType.objects.get_for_model(self).pk,object_id=self.id):
            self.hours_donated += comment.hours_donated
            self.hours_claimed += comment.hours_claimed
            self.hours_matched += Decimal(2.)*comment.hours_matched
        self.save()

    def get_usd(self):
        return self.hours_donated*HourValue.objects.latest('created_at').value


class Work(models.Model):
    personal = models.BooleanField(default=False)
    language = models.ForeignKey(
        'Language',
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        'Task',
        related_name='task_works',
        blank=False,
        null=False,
    )
    name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )
    url = models.URLField(
        max_length=150,
        unique=False,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    commented_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_works',
        blank=False,
        null=False,
    )
    file = models.FileField(
        null=True,
        upload_to='files',
        blank=True,
    )
    parent_work_id = models.PositiveIntegerField(
        unique=False,
        null=True,
        blank=True,
    )
    description = MarkdownField(blank=False)
    hours_donated = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_claimed = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_matched = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"

    def sum_hours(self):
        self.hours_donated = Decimal(0.)
        self.hours_claimed = Decimal(0.)
        self.hours_matched = Decimal(0.)
        for comment in Comment.objects.filter(content_type__pk=\
            ContentType.objects.get_for_model(self).pk,object_id=self.id):
            self.hours_donated += comment.hours_donated
            self.hours_claimed += comment.hours_claimed
            self.hours_matched += Decimal(2.)*comment.hours_matched
        self.save()

    def get_usd(self):
        return self.hours_donated*HourValue.objects.latest('created_at').value


class Idea(models.Model):
    description = MarkdownField(blank=False)
    language = models.ForeignKey(
        'Language',
        blank=True,
        null=True,
    )
    personal = models.BooleanField(default=False)
    name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    commented_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    summary = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_ideas',
        blank=False,
        null=False,
    )
    goal = models.ForeignKey(
        'Goal',
        related_name='goal_ideas',
        blank=False,
        null=False,
    )
    hours_donated = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_claimed = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_matched = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"

    def sum_hours(self):
        self.hours_donated = Decimal(0.)
        self.hours_claimed = Decimal(0.)
        self.hours_matched = Decimal(0.)
        for comment in Comment.objects.filter(content_type__pk=\
            ContentType.objects.get_for_model(self).pk,object_id=self.id):
            self.hours_donated += comment.hours_donated
            self.hours_claimed += comment.hours_claimed
            self.hours_matched += Decimal(2.)*comment.hours_matched
        self.save()

    def get_usd(self):
        return self.hours_donated*HourValue.objects.latest('created_at').value


class Step(models.Model):
    personal = models.BooleanField(default=False)
    language = models.ForeignKey(
        'Language',
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_steps',
        blank=False,
        null=False,
    )
    name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    commented_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    deliverables = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )
    priority = models.IntegerField(
        unique=False,
        null=False,
        blank=False,
    )
    plan = models.ForeignKey(
        'Plan',
        related_name='plan_steps',
        blank=False,
        null=False,
    )
    objective = MarkdownField(blank=False)
    investables = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )
    hours_donated = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_claimed = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_matched = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"

    def sum_hours(self):
        self.hours_donated = Decimal(0.)
        self.hours_claimed = Decimal(0.)
        self.hours_matched = Decimal(0.)
        for comment in Comment.objects.filter(content_type__pk=\
            ContentType.objects.get_for_model(self).pk,object_id=self.id):
            self.hours_donated += comment.hours_donated
            self.hours_claimed += comment.hours_claimed
            self.hours_matched += Decimal(2.)*comment.hours_matched
        self.save()

    def get_usd(self):
        return self.hours_donated*HourValue.objects.latest('created_at').value


class Task(models.Model):
    personal = models.BooleanField(default=False)
    language = models.ForeignKey(
        'Language',
        blank=True,
        null=True,
    )
    name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    commented_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    priority = models.IntegerField(
        unique=False,
        null=False,
        blank=False,
    )
    step = models.ForeignKey(
        'Step',
        related_name='step_tasks',
        blank=False,
        null=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_tasks',
        blank=False,
        null=False,
    )
    hours_donated = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_claimed = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_matched = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"

    def sum_hours(self):
        self.hours_donated = Decimal(0.)
        self.hours_claimed = Decimal(0.)
        self.hours_matched = Decimal(0.)
        for comment in Comment.objects.filter(content_type__pk=\
            ContentType.objects.get_for_model(self).pk,object_id=self.id):
            self.hours_donated += comment.hours_donated
            self.hours_matched += Decimal(2.)*comment.hours_matched
            self.hours_claimed += comment.hours_claimed
        self.save()

    def get_usd(self):
        return self.hours_donated*HourValue.objects.latest('created_at').value


class Need(models.Model):
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    commented_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    defined_meaning_id = models.PositiveIntegerField(null=True, blank=True)
    definition = models.CharField(max_length=255)
    type = models.ForeignKey(
        'Type',
        blank=True,
        null=True,
    )
    language = models.ForeignKey(
        'Language',
        blank=True,
        null=True,
    )
    name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_needs',
        blank=False,
        null=False,
    )
    hours_donated = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_claimed = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_matched = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"

    class Meta:
        unique_together = ('language', 'name', 'definition')

    def sum_hours(self):
        self.hours_donated = Decimal(0.)
        self.hours_claimed = Decimal(0.)
        self.hours_matched = Decimal(0.)
        for comment in Comment.objects.filter(content_type__pk=\
            ContentType.objects.get_for_model(self).pk,object_id=self.id):
            self.hours_donated += comment.hours_donated
            self.hours_claimed += comment.hours_claimed
            self.hours_matched += Decimal(2.)*comment.hours_matched
        self.save()

    def get_usd(self):
        return self.hours_donated*HourValue.objects.latest('created_at').value


class Type(models.Model):
    name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"


class Plan(models.Model):
    personal = models.BooleanField(default=False)
    language = models.ForeignKey(
        'Language',
        blank=True,
        null=True,
    )
    name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
        verbose_name='means'
    )
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    commented_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    idea = models.ForeignKey(
        'Idea',
        related_name='idea_plans',
        blank=False,
        null=False,
    )
    deliverable = MarkdownField(blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_plans',
        blank=False,
        null=False,
    )
    situation = MarkdownField(blank=False)
    hours_donated = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_claimed = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    hours_matched = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"

    def sum_hours(self):
        self.hours_donated = Decimal(0.)
        self.hours_claimed = Decimal(0.)
        self.hours_matched = Decimal(0.)
        for comment in Comment.objects.filter(content_type__pk=\
            ContentType.objects.get_for_model(self).pk,object_id=self.id):
            self.hours_donated += comment.hours_donated
            self.hours_claimed += comment.hours_claimed
            self.hours_matched += Decimal(2.)*comment.hours_matched
        self.save()
    

    def get_usd(self):
        return self.hours_donated*HourValue.objects.latest('created_at').value


class Language(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    http_accept_language = models.CharField(max_length=255, blank=True,
                                            null=True)
    omegawiki_language_id = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        try:
            return unicode(self.name[:50])
        except TypeError:
            return unicode(self.pk)

# Signals register place
#post_save.connect(_comment_post_save, sender=Comment)
