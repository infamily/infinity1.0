from django.conf import settings
from django.db import models


class BaseContentModel(models.Model):
    is_link = models.BooleanField(default=False)
    is_historical = models.BooleanField(default=False)
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
    commented_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        unique=False,
        null=False,
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
    hours_assumed = models.DecimalField(
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
    name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_%(class)ss',
        blank=False,
        null=False,
    )

    personal = models.BooleanField(default=False)

    sharewith = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True
    )

    language = models.ForeignKey(
        'Language',
        blank=True,
        null=True,
    )

    total_donated = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    total_claimed = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    total_assumed = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    total_matched = models.DecimalField(
        default=0.,
        decimal_places=8,
        max_digits=20,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        unique=False,
        null=False,
        blank=False,
    )

    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="%(class)s_subscribers"
    )

    def sum_hours(self):
        self.hours_donated = Decimal(0.)
        self.hours_claimed = Decimal(0.)
        self.hours_assumed = Decimal(0.)
        self.hours_matched = Decimal(0.)
        comment_content_type = ContentType.objects.get_for_model(self)
        comments = Comment.objects.filter(
            content_type__pk=comment_content_type.pk,
            object_id=self.id
        )
        for comment in comments:
            self.hours_donated += comment.hours_donated
            self.hours_claimed += comment.hours_claimed
            self.hours_assumed += comment.hours_assumed
            self.hours_matched += Decimal(2.)*comment.hours_matched
        self.save()

    def sum_totals(self):
        self.total_donated = self.hours_donated
        self.total_claimed = self.hours_claimed
        self.total_assumed = self.hours_assumed
        self.total_matched = self.hours_matched
        if hasattr(self,'definition_goals'):
            child_objects = self.definition_goals.all()
        elif hasattr(self,'need_goals'):
            child_objects = self.definition_goals.all()
        elif hasattr(self,'goal_ideas'):
            child_objects = self.goal_ideas.all()
        elif hasattr(self,'idea_plans'):
            child_objects = self.idea_plans.all()
        elif hasattr(self, 'plan_steps'):
            child_objects = self.plan_steps.all()
        elif hasattr(self, 'step_tasks'):
            child_objects = self.step_tasks.all()
        elif hasattr(self, 'task_works'):
            child_objects = self.task_works.all()
        if 'child_objects' in locals():
            for content in child_objects:
                self.total_donated += content.total_donated
                self.total_claimed += content.total_claimed
                self.total_assumed += content.total_assumed
                self.total_matched += content.total_matched
        self.save()

    def get_remain_usd(self):
        return ((self.total_assumed+self.total_claimed)-self.total_donated)*\
            HourValue.objects.latest('created_at').value

    def not_funded_hours(self):
        return self.total_assumed+self.total_claimed-self.total_donated

    def comment_count(self):
        comment_content_type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(
            content_type__pk=comment_content_type.pk,
            object_id=self.id
        ).count()

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        return "/"

    def get_usd(self):
        return self.total_donated*HourValue.objects.latest('created_at').value

    def translations(self):
        """
        Returns False if there is no translation
        """
        content_type = ContentType.objects.get_for_model(self)
        translations = Translation.objects.filter(
            content_type=content_type,
            object_id=self.pk
        ).exclude(default=True)

        return translations

    class Meta:
        abstract = True
