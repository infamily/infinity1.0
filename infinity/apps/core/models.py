from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_superuser, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_superuser=is_superuser,
            is_staff=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, **extra_fields)


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(blank=False)
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
        'User',
        blank=False,
        null=False,
    )

    def __unicode__(self):
        return u"Comment #%s" % self.id

    def get_absolute_url(self):
        return "/"


class Goal(models.Model):
    name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )
    personal = models.BooleanField(default=True)
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
    reason = models.TextField(blank=False)
    user = models.ForeignKey(
        'User',
        blank=False,
        null=False,
    )
    need = models.ForeignKey(
        'Need',
        blank=False,
        null=False,
    )
    quantity = models.PositiveIntegerField(
        unique=False,
        null=False,
        blank=False,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"


class Work(models.Model):
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
    user = models.ForeignKey(
        'User',
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
    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"


class Idea(models.Model):
    description = models.TextField(blank=False)
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
    summary = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )
    user = models.ForeignKey(
        'User',
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

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"


class Step(models.Model):
    user = models.ForeignKey(
        'User',
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
    objective = models.TextField(blank=False)
    investables = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"


class Task(models.Model):
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
        'User',
        related_name='user_tasks',
        blank=False,
        null=False,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"


class User(AbstractBaseUser, PermissionsMixin):
    introduction = models.TextField(blank=False)
    email = models.EmailField(
        max_length=150,
        unique=False,
        null=False,
        blank=False,
    )
    is_staff = models.BooleanField(default=False, editable=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return unicode(self)

    def get_short_name(self):
        return unicode(self)

    def __unicode__(self):
        return unicode(self.email)

    def get_absolute_url(self):
        return "/"


class Need(models.Model):
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    type = models.ForeignKey(
        'Type',
        blank=True,
        null=True,
    )
    name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"


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
    idea = models.ForeignKey(
        'Idea',
        related_name='idea_plans',
        blank=False,
        null=False,
    )
    deliverable = models.TextField(blank=False)
    user = models.ForeignKey(
        'User',
        related_name='user_plans',
        blank=False,
        null=False,
    )
    situation = models.TextField(blank=False)

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"
