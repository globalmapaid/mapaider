import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    uuid = models.UUIDField(_('uuid'), default=uuid.uuid4, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # class Meta:
    #     verbose_name = _('user')
    #     verbose_name_plural = _('users')
    #     app_label = 'auth'

    def __str__(self):
        return self.email


