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
    day_condition = models.CharField(max_length=8)
    created_at = models.DateTimeField(default=timezone.now)
    #place = models.CharField(max_length=8)
    #day = models.CharField(max_length=8)
    #month = models.CharField(max_length=8)
    #月、日付、場所、空き状況、更新日

    def __str__(self):
        return self.day_condition
