from django.db import models
import datetime
from django.utils import timezone


class Group(models.Model):
    host = models.CharField(max_length=10)
    pub_date = models.DateTimeField("date published")

class UserName(models.Model):
    user_name = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_name



