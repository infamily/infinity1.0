from django.db import models
from django.db.models import signals
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, PermissionsMixin
)


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


class Relationship(models.Model):
    from_person = models.ForeignKey('User', related_name='from_people')
    to_person = models.ForeignKey('User', related_name='to_people')


class User(AbstractUser):
    about = models.TextField(blank=True)
    friends = models.ManyToManyField('self', symmetrical=False, through='Relationship')

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

    def add_relationship(self, person, symm=False):
        """ Add relationship with symmetrical False by default
        """
        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person,
        )

        if symm:
            person.add_relationship(self, True)

        return relationship

    def remove_relationship(self, person, symm=False):
        """ Remove relationship with symmetrical False
        """
        Relationship.objects.filter(
            from_person=self,
            to_person=person,
        ).delete()
        if symm:
            # avoid recursion by passing `symm=True`
            person.remove_relationship(self, True)

    def get_relationships(self):
        """ Get all user relationships
        """
        return self.friends.filter(
            to_people__from_person=self
        )

    def have_relationship_with(self, person):
        """ Get relationship between users
        """
        rel = self.get_relationships().filter(
            to_people__to_person=person,
            from_people__from_person=person
        )

        return rel.exists()


from .signals import user_post_save
signals.post_save.connect(user_post_save, sender=User)
