from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    objects = CustomUserManager()


