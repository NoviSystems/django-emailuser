
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django import get_version

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from emailuser import fields


class EmailUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **kwargs):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, date_joined=now, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves an EmailUser with the given email and password.
        """
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        return self._create_user(email, password, True, True, **extra_fields)


class AbstractEmailUser(AbstractBaseUser, PermissionsMixin):
    """
    Abstract user class that mimics Django's default User, but
    without a username field.

    Password and email are required. Other fields are optional.
    """
    email = fields.EmailField(_('email address'), max_length=254, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = EmailUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """Returns the full email address."""
        return self.email

    def get_short_name(self):
        """Returns the local part of the email address."""
        return self.email.split('@')[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


def min_version(actual, minimum):
    try:
        from distutils.version import NormalizedVersion as Version
    except:
        from distutils.version import LooseVersion as Version

    return Version(actual) > Version(minimum)


# Django 1.6 bug - https://code.djangoproject.com/ticket/21419
# Two concrete sub classes of the same abstract base user model will conflict and cause
# validation to fail if their abc inherits from PermissionsMixin.
if min_version(get_version(), '1.7'):

    class EmailUser(AbstractEmailUser):
        """
        Users within the Django authentication system are represented by this
        model.

        Username, password and email are required. Other fields are optional.
        """
        class Meta:
            verbose_name = _('user')
            verbose_name_plural = _('users')
