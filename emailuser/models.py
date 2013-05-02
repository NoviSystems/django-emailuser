
from django.core.mail import send_mail
from django.db import models
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


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
    email = models.EmailField(_('email address'), max_length=255, unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = EmailUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email.replace("@", "_"))

    def get_full_name(self):
        """Returns the full name or the full email address
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip() or self.email

    def get_short_name(self):
        """Returns the first name or the local part of the email address.
        """
        return self.first_name or self.email.split('@')[0]

    def email_user(self, subject, message, from_email=None):
        """Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


class EmailUser(AbstractEmailUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username, password and email are required. Other fields are optional.
    """
    class Meta:
        app_label = 'auth'
        verbose_name = _('user')
        verbose_name_plural = _('users')


class EmailUserExt(AbstractEmailUser):
    """Example extension class. Provides helper methods for getting FK'd
    profile classes.
    """
    class Meta:
        app_label = 'auth'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def is_a(self, cls):
        try:
            return len(cls.objects.filter(user=self.user)) > 0
        except Exception:
            return False

    @property
    def get(self, cls):
        try:
            return cls.objects.filter(user=self.user)[0]
        except Exception:
            return None
