from django.contrib.auth.models import AbstractUser
from django.db.models import CharField

from django.db import models


class User(AbstractUser):
    phone = CharField(max_length=11, null=True, unique=True)

    @property
    def full_name(self):
        if len(self.get_full_name()) == 0:
            return self.username
        return self.get_full_name()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
