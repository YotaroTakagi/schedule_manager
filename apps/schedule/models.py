from django.db import models


class Group(models.Model):
    host = models.CharField(max_length=10)
    pub_date = models.DateTimeField("date published")
