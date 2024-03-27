from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    meetup_api_key = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username


class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.group_name} ({self.group_id})"
