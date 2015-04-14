from django.core.mail import send_mail
from django.db import models
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from emailuser import fields


class EmailUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves an EmailUser with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = EmailUserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


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
        abstract = True

    def get_absolute_url(self):
        email = self.email.split("@")
        return "/users/%s/%s" % (urlquote(email[1]), urlquote(email[0]),)

    def get_full_name(self):
        """Returns the full email address."""
        return self.email

    def get_short_name(self):
        """Returns the local part of the email address."""
        return self.email.split('@')[0]

    def email_user(self, subject, message, from_email=None):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email])


# Django 1.6 bug - https://code.djangoproject.com/ticket/21419
# Two concrete sub classes of the same abstract base user model will conflict and cause
# validation to fail if their abc inherits from PermissionsMixin. Lame.

# class EmailUser(AbstractEmailUser):
#     """
#     Users within the Django authentication system are represented by this
#     model.
#
#     Username, password and email are required. Other fields are optional.
#     """
#     class Meta:
#         app_label = 'auth'
#         verbose_name = _('user')
#         verbose_name_plural = _('users')
