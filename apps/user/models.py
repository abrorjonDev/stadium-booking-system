import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.utils.translation import gettext_lazy as _

from .manager import UserManager


class RoleChoice(models.TextChoices):
    ADMIN = 'admin', _('Admin')
    OWNER = 'owner', _('Owner')
    USER = 'user', _('User')


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(choices=RoleChoice.choices,default=RoleChoice.USER,max_length=10)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    @property
    def is_staff(self):
        return self.is_admin
