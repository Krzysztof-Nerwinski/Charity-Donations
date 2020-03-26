from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _

from apps.accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('użytkownik')
        verbose_name_plural = _('użytkownicy')

