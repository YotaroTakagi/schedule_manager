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

class ScheduleCondition(models.Model):
    month = models.CharField(max_length=8, null=True)
    day = models.CharField(max_length=8, null=True)
    time = models.CharField(max_length=8, null=True)
    day_condition = models.CharField(max_length=8, default="予約不可")
    place = models.CharField(max_length=8, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    user_name = models.CharField(max_length=8, null=True)

    def __str__(self):
        return self.day_condition
